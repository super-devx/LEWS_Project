#!/usr/bin/python3
import sys
import time
import os
import select
import socket
import json
import glob
from datetime import datetime
import NodeValue
import serial
import termios

SERIAL_BAUD = 115200
SERVER_IP = "103.37.200.35"
SERVER_PORT = 5000
SOCKET_TIMEOUT = 10
MAX_RETRIES = 5
INITIAL_BACKOFF = 2  # seconds

# Use the script's own directory for log files so there are no permission issues
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, 'log.txt')
UNSENT_FILE = os.path.join(SCRIPT_DIR, 'unsent_data.txt')
BACKUP_FILE = os.path.join(SCRIPT_DIR, 'all_received_data.txt')

global ser
global received_data
received_data = ""


def log(msg):
  """Print a timestamped, flush-safe log message."""
  print('[%s] %s' % (datetime.now().strftime('%H:%M:%S'), msg), flush=True)


def find_serial_port():
  """Find the correct serial port by scanning all available /dev/ttyUSB* devices."""
  ports = sorted(glob.glob('/dev/ttyUSB*'))
  if not ports:
    log('SERIAL | No USB devices found')
    return None
  log('SERIAL | Scanning ports: %s' % ', '.join(ports))
  for port in ports:
    try:
      s = serial.Serial(port, SERIAL_BAUD, timeout=2)
      s.close()
      return port
    except Exception:
      continue
  return None


# --- Connect to serial port ---
log('========== STARTING UP ==========')
ser = None
while ser is None:
  try:
    port = find_serial_port()
    if port:
      ser = serial.Serial(port, SERIAL_BAUD)
      log('SERIAL | Connected on %s' % port)
    else:
      time.sleep(1)
  except Exception as e:
    log('SERIAL | Connection failed: %s' % e)
    time.sleep(1)


def log_to_file(message):
  """Safely write a message with timestamp to the log file."""
  try:
    with open(LOG_FILE, 'a+') as f:
      f.write('%s %s\n' % (datetime.now(), message))
  except Exception:
    log('WARNING | Could not write to log file')


def save_backup(data):
  """Save every received data packet to backup file, regardless of send status."""
  try:
    with open(BACKUP_FILE, 'a+') as f:
      f.write('%s|%s\n' % (datetime.now(), data))
  except Exception:
    log('WARNING | Could not write to backup file')


def buffer_unsent_data(data):
  """Save data that could not be sent so it can be retried later."""
  try:
    with open(UNSENT_FILE, 'a+') as f:
      f.write('%s|%s\n' % (datetime.now(), data))
  except Exception:
    log('WARNING | Could not buffer unsent data')


def send_to_server(data):
  """Send data to server with retry and exponential backoff. Returns True on success."""
  backoff = INITIAL_BACKOFF
  for attempt in range(MAX_RETRIES):
    try:
      host = socket.gethostbyname(SERVER_IP)
      conn = socket.create_connection((host, SERVER_PORT), SOCKET_TIMEOUT)
      conn.sendall(bytes(data, 'utf-8'))
      conn.close()
      return True
    except Exception as e:
      log('SEND   | Attempt %d/%d failed: %s' % (attempt + 1, MAX_RETRIES, e))
      if attempt < MAX_RETRIES - 1:
        log('SEND   | Retrying in %ds...' % backoff)
        time.sleep(backoff)
        backoff = min(backoff * 2, 60)
  return False


def flush_unsent_data():
  """Try to send any previously buffered data."""
  try:
    if not os.path.exists(UNSENT_FILE):
      return
    with open(UNSENT_FILE, 'r') as f:
      lines = f.readlines()
    if not lines:
      return

    log('BUFFER | Flushing %d buffered packets...' % len(lines))
    remaining = []
    sent = 0
    for line in lines:
      line = line.strip()
      if not line:
        continue
      parts = line.split('|', 1)
      if len(parts) == 2:
        data = parts[1]
        if send_to_server(data):
          sent += 1
        else:
          remaining.append(line)

    with open(UNSENT_FILE, 'w') as f:
      for line in remaining:
        f.write(line + '\n')
    log('BUFFER | Flushed %d, remaining %d' % (sent, len(remaining)))
  except Exception as e:
    log('WARNING | Could not flush unsent data: %s' % e)


def reconnect_serial():
  """Reconnect to the serial port, scanning all available USB ports."""
  global ser
  backoff = 1
  while True:
    try:
      port = find_serial_port()
      if port:
        ser = serial.Serial(port, SERIAL_BAUD)
        log('SERIAL | Reconnected on %s' % port)
        return
      else:
        log('SERIAL | Waiting for device... retrying in %ds' % backoff)
    except Exception as e:
      log('SERIAL | Reconnect failed: %s, retrying in %ds' % (e, backoff))
    time.sleep(backoff)
    backoff = min(backoff * 2, 30)


# --- Main loop ---
send_failures = 0
packet_count = 0

while True:
    try:
      ser.flush()
      time.sleep(1)

      data = ser.read()
      time.sleep(0.05)
      data_left = ser.inWaiting()
      data += ser.read(data_left)
      received_data = data.decode()

      index_strt = received_data.find('&')
      index_end = received_data.find('!')

      if (index_end == -1 or index_strt == -1 or
          received_data.count('@') != 2 or
          received_data[-1] != '!' or
          received_data.count('!') != 1 or
          received_data.count('&') != 1):
        continue

      received_data = received_data[index_strt + 1:index_end]
      packet_count += 1
      log('RECV   | #%d | %s' % (packet_count, received_data))

      # Always save to backup first — this is the data safety net
      save_backup(received_data)

      c = NodeValue.ContentFromClient(received_data)
      c.sensorvalues()

      # Try to flush old buffered data first (piggyback on connectivity)
      flush_unsent_data()

      # Send current data
      if send_to_server(received_data):
        send_failures = 0
        log('SEND   | OK | #%d sent to %s:%d' % (packet_count, SERVER_IP, SERVER_PORT))
      else:
        send_failures += 1
        log('SEND   | FAILED | #%d buffered locally (total failures: %d)' % (packet_count, send_failures))
        log_to_file('SEND FAILED: ' + received_data)
        buffer_unsent_data(received_data)

    except (serial.SerialException, termios.error, OSError) as e:
      log('SERIAL | DISCONNECTED: %s' % e)
      log_to_file('SERIAL ERROR: ' + str(e))
      reconnect_serial()
      received_data = ""

    except Exception as e:
      log('ERROR  | %s' % e)
      log_to_file(str(e))
      if len(received_data) > 10:
        log_to_file('UNSENT: ' + received_data)
        buffer_unsent_data(received_data)
      received_data = ""
