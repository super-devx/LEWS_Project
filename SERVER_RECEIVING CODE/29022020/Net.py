# This is the latest code till 25/05/2020
import select
import socket
import sys
import threading
import Sensorinformation
import NodeValue
from datetime import datetime

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(0)

# Bind the socket to the port
server_address = ('localhost', 5000)
# server_address = ('10.13.1.211', 5000)
server_address = ('192.168.104.84', 5000)
server.bind(server_address)

# Listen for incoming connections
server.listen(128)

inputs = [server]
outputs = []

print('[SERVER] Listening on %s:%d' % (server_address[0], server_address[1]))


def process_data_async(process_data):
    """Process received data in a separate thread so the select loop stays responsive."""
    try:
        c = NodeValue.ContentFromClient(process_data)
        c.sensorvalues()

        with open('A.txt', 'a+') as f:
            now = datetime.now()
            f.write('%s' % now)
            f.write("\r\n")
            f.write(process_data)
            if process_data[-1] == ')':
                f.write('\n')
    except Exception as e:
        print('[ERROR] Processing failed: %s' % e)


while inputs:
    readable, writable, exceptional = select.select(inputs, outputs, inputs, 1)
    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            connection.setblocking(0)
            inputs.append(connection)
        else:
            try:
                data = s.recv(2000)

                if data:
                    process_data = data.decode('utf-8').lower()
                    if process_data.startswith("get"):
                        continue
                    print('[RECV] %d bytes | %s' % (len(process_data), process_data[:80]))

                    # Process in a worker thread to keep the select loop free
                    t = threading.Thread(target=process_data_async, args=(process_data,))
                    t.daemon = True
                    t.start()
                else:
                    inputs.remove(s)
                    s.close()

            except Exception as e:
                print('[ERROR] Client socket: %s' % e)
                if s in inputs:
                    inputs.remove(s)
                s.close()

    for s in exceptional:
        print('[ERROR] Exceptional condition on socket')
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

