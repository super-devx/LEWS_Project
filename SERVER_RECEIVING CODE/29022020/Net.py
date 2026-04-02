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

print('waiting for request')


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
        print('WRITTEN IN DATA')
        print(process_data)
    except Exception as e:
        print('Processing error: %s' % e)


while inputs:
    readable, writable, exceptional = select.select(inputs, outputs, inputs, 1)
    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            connection.setblocking(0)
            inputs.append(connection)
            print('connection done')
        else:
            try:
                data = s.recv(2000)
                print('I have received data')

                if data:
                    print('DATA RECEIVED')
                    process_data = data.decode('utf-8').lower()
                    print(process_data)
                    print(len(process_data))
                    if process_data.startswith("get"):
                        continue

                    # Process in a worker thread to keep the select loop free
                    t = threading.Thread(target=process_data_async, args=(process_data,))
                    t.daemon = True
                    t.start()
                else:
                    inputs.remove(s)
                    s.close()
                    print('out')

            except Exception as e:
                print('in', e)
                if s in inputs:
                    inputs.remove(s)
                s.close()

    for s in exceptional:
        print('i am in exceptional')
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

    for item in inputs:
        # print(item)
        pass
