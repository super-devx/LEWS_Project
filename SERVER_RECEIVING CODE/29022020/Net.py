import select
import socket
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
import Sensorinformation
import NodeValue
from datetime import datetime

# Force unbuffered stdout so logs never appear "stuck".
# Without this, Python block-buffers stdout when not attached to an interactive
# terminal (nohup, screen, pipe). Prints accumulate silently in a memory buffer
# and only appear when it fills (~4-8 KB) or the process exits / receives Ctrl+C.
sys.stdout.reconfigure(line_buffering=True)

# Shared lock for all print/log calls across threads to prevent interleaved output
_print_lock = threading.Lock()
# Workers now run truly in parallel, so concurrent append-mode writes to A.txt
# can interleave on some platforms. Serialize them.
_file_lock = threading.Lock()

# Bounded worker pool. Caps thread count even under sustained DB stalls so the
# main select loop keeps getting CPU and the listen backlog never overflows.
# max_workers matches NodeValue._DB_POOL.maxconn so workers don't starve on getconn().
_worker_pool = ThreadPoolExecutor(max_workers=16, thread_name_prefix="ingest")


def log(msg):
    """Timestamped, thread-safe log."""
    with _print_lock:
        print('[%s] %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg), flush=True)


# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(0)

# Bind the socket to the port
server_address = ('localhost', 5000)
# server_address = ('10.13.1.211', 5000)
server_address = ('192.168.104.84', 5000)
server.bind(server_address)

# Listen for incoming connections. SOMAXCONN gives the kernel's max queue —
# margin for bursty arrivals (e.g. all Pis reconnecting after a network blip).
server.listen(socket.SOMAXCONN)

inputs = [server]
outputs = []

log('SERVER started on %s:%d' % (server_address[0], server_address[1]))


def process_data_async(process_data):
    """Process received data in a separate thread so the select loop stays responsive."""
    try:
        # Data format from Pi: "YYYY-MM-DD HH:MM:SS|sensordata"
        # If timestamp prefix is present, extract it as the Pi's receive_time
        if '|' in process_data:
            pi_timestamp_str, sensor_data = process_data.split('|', 1)
            try:
                pi_timestamp = datetime.strptime(pi_timestamp_str.strip(), '%Y-%m-%d %H:%M:%S')
            except ValueError:
                # Malformed timestamp, fall back to server time
                sensor_data = process_data
                pi_timestamp = datetime.now()
        else:
            # Backwards compatibility: no timestamp prefix
            sensor_data = process_data
            pi_timestamp = datetime.now()

        c = NodeValue.ContentFromClient(sensor_data, pi_timestamp)
        c.sensorvalues()

        with _file_lock:
            with open('A.txt', 'a+') as f:
                now = datetime.now()
                f.write('%s' % now)
                f.write("\r\n")
                f.write(sensor_data)
                if sensor_data[-1] == ')':
                    f.write('\n')
        log('SAVED to A.txt | %s' % sensor_data[:60])
    except Exception as e:
        log('ERROR processing data: %s' % e)


active_connections = 0

try:
    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs, 1)
        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                connection.setblocking(0)
                inputs.append(connection)
                active_connections += 1
                log('CONNECT from %s:%d | active=%d' % (client_address[0], client_address[1], active_connections))
            else:
                try:
                    data = s.recv(2000)

                    if data:
                        process_data = data.decode('utf-8').lower()
                        if process_data.startswith("get"):
                            continue
                        log('RECV %d bytes | %s' % (len(process_data), process_data[:80]))

                        # Submit to the bounded worker pool. Falls back to running
                        # inline if the executor is shutting down.
                        try:
                            _worker_pool.submit(process_data_async, process_data)
                        except RuntimeError:
                            process_data_async(process_data)
                    else:
                        inputs.remove(s)
                        s.close()
                        active_connections -= 1
                        log('DISCONNECT | active=%d' % active_connections)

                except Exception as e:
                    log('ERROR on client socket: %s' % e)
                    if s in inputs:
                        inputs.remove(s)
                    s.close()
                    active_connections -= 1

        for s in exceptional:
            log('ERROR exceptional condition on socket')
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            active_connections -= 1
except KeyboardInterrupt:
    log('SHUTDOWN requested')
finally:
    try:
        server.close()
    except Exception:
        pass
    # Drop queued work; in-flight tasks have a 10s statement_timeout backstop.
    _worker_pool.shutdown(wait=False, cancel_futures=True)
    NodeValue.shutdown_pool()
    log('SHUTDOWN complete')
