#!/usr/bin/python3
import sys
print('NEW DATA..................................')
import time
import os
import select
import socket
import json
from datetime import datetime
import NodeValue
import serial

SERIAL_PORT = '/dev/ttyUSB7'
SERIAL_BAUD = 115200
SERVER_IP = "103.37.200.35"
SERVER_PORT = 5000
SOCKET_TIMEOUT = 10
LOG_FILE = '/home/sailab/ProjectCode/log.txt'
UNSENT_FILE = '/home/sailab/ProjectCode/unsent_data.txt'
MAX_RETRIES = 5
INITIAL_BACKOFF = 2  # seconds

global ser
global received_data
received_data = ""

# --- Connect to serial port ---
ser = None
while ser is None:
  try:
    ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD)
    print('CONNECTED TO SL')
  except Exception as e:
    print('NOT CONNECTED TO SL')
    time.sleep(1)


def log_to_file(message):
  """Safely write a message with timestamp to the log file."""
  try:
    with open(LOG_FILE, 'a+') as f:
      f.write('%s %s\n' % (datetime.now(), message))
  except Exception:
    print('WARNING: Could not write to log file')


def buffer_unsent_data(data):
  """Save data that could not be sent so it can be retried later."""
  try:
    with open(UNSENT_FILE, 'a+') as f:
      f.write('%s|%s\n' % (datetime.now(), data))
  except Exception:
    print('WARNING: Could not buffer unsent data')


def send_to_server(data):
  """Send data to server with retry and exponential backoff. Returns True on success."""
  backoff = INITIAL_BACKOFF
  for attempt in range(MAX_RETRIES):
    try:
      host = socket.gethostbyname(SERVER_IP)
      conn = socket.create_connection((host, SERVER_PORT), SOCKET_TIMEOUT)
      conn.sendall(bytes(data, 'utf-8'))
      conn.close()
      print("data send")
      return True
    except Exception as e:
      print('Send attempt %d/%d failed: %s' % (attempt + 1, MAX_RETRIES, e))
      if attempt < MAX_RETRIES - 1:
        print('Retrying in %d seconds...' % backoff)
        time.sleep(backoff)
        backoff = min(backoff * 2, 60)  # cap at 60 seconds
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

    remaining = []
    for line in lines:
      line = line.strip()
      if not line:
        continue
      # Format: timestamp|data
      parts = line.split('|', 1)
      if len(parts) == 2:
        data = parts[1]
        if send_to_server(data):
          print('Flushed buffered data: %s' % data[:50])
        else:
          remaining.append(line)

    # Rewrite file with only the lines that still failed
    with open(UNSENT_FILE, 'w') as f:
      for line in remaining:
        f.write(line + '\n')
  except Exception as e:
    print('WARNING: Could not flush unsent data: %s' % e)


def reconnect_serial():
  """Reconnect to the serial port with retries."""
  global ser
  backoff = 1
  while True:
    try:
      ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD)
      print('Serial reconnected on %s' % SERIAL_PORT)
      return
    except Exception as e:
      print('Serial reconnect failed: %s, retrying in %ds' % (e, backoff))
      time.sleep(backoff)
      backoff = min(backoff * 2, 30)


# --- Main loop ---
send_failures = 0

while True:
    try:
      print('waiting on serial')
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
      print(received_data)
      time.sleep(1)

      c = NodeValue.ContentFromClient(received_data)
      c.sensorvalues()

      # Try to flush old buffered data first (piggyback on connectivity)
      flush_unsent_data()

      # Send current data
      if send_to_server(received_data):
        send_failures = 0
      else:
        print('DATA CANT SEND after %d retries, buffering locally' % MAX_RETRIES)
        log_to_file('SEND FAILED: ' + received_data)
        buffer_unsent_data(received_data)
        send_failures += 1

    except serial.SerialException as e:
      print('Serial error: %s' % e)
      log_to_file('SERIAL ERROR: ' + str(e))
      reconnect_serial()
      received_data = ""

    except Exception as e:
      print('Error: %s' % e)
      log_to_file(str(e))
      if len(received_data) > 10:
        log_to_file('UNSENT: ' + received_data)
        buffer_unsent_data(received_data)
      received_data = ""
