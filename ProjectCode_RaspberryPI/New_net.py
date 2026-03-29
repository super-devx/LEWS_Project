#!/usr/bin/python3
import sys
print('NEW DATA..................................')
#print(sys.version)
import time
import os
import select
import socket
import json
#import httplib
#import urllib
from datetime import datetime
import NodeValue
import serial
s=True
global ser
global received_data
while(s):
  try:
    #ser.flush()
    ser = serial.Serial('/dev/ttyUSB7', 115200)
    print('connectedamrita')
    s=False
  except Exception as e:
    print('NOT CONNECTED TO SL')
    s=True
    #ser.flush()
    time.sleep(1)

#from wireless import Wireless
#wire = Wireless('wlan0')
#try:
# status =wire.connect(ssid='HUAWEI-9F29',password='Root@123')
# if status == True:
#  print("NET IS PROPERLY CONNECTED")
 #else:
 # print("NET IS NOT CONNECTED")
#except:
# print('ANY ISSUE IN NETWORKING')   #print('i have came here')
#temp=''

###try:

  ###from Net_email import Emailer
  ###Emailer().sendmail('amritajoshi.er@gmail.com','NHMS','SERVER HAS BEEN STARTED')
  ###print('MAIL SENT')
###except Exception as e:
  ###print("mail cant send",e)
  ###f1 = open("/home/pi/Desktop/latest/error1.txt", "w+")
  ###now1 = datetime.now()
  ###f1.write(str(e))
  ###f1.write(' ')
  ###f1.write('%s'%now1)
  ###f1.write("\r\n")
  ###f1.close()

while(True):
    try:

      print('waiting on serial')
      ser.flush()
      time.sleep(1)


      data = ser.read() # Read the newest output
      #data = b"&c1@netala@n2(moisture1:56.48)(voltage1:3.66)(vols1:2269.00)(pitch1:-85)(roll1:-12)(pitch2:24)(roll2:-68)(pitch3:86)(roll3:1)(pitch4:1)(roll4:84)!" # Read the newest output
      #print(data)
      time.sleep(0.05)
      data_left = ser.inWaiting()
      data += ser.read(data_left)
      #print(received_data,'is received from Sensor')
      received_data = data.decode()
      #received_data="tch2:-95)(roll2:-95)(pitch3:18)(roll3:-74)(pitch4:-95)(roll4:-95)!"
      index_strt=received_data.find('&')
      index_end=received_data.find('!')
      l=len(received_data);
      #if(index_end!=-1 and index_strt!=-1):
        #temp=''
      if(index_end==-1 or index_strt==-1 or received_data.count('@')!=2 or received_data[-1]!='!' or received_data.count('!')!=1  or received_data.count('&')!=1):
        #temp=''
        continue
      #if(index_end!=-1 and index_strt>index_end):
        #temp=''
        #continue;
      #if(index_end==-1):
        #temp=received_data
        #continue;#
        #print('i am in loop2')
        #print (received_Data)
      #received_data=temp+received_data
      #temp=''
      received_data=received_data[index_strt+1:index_end]
      #f=open('/home/sailab/ProjectCode','a+')
      #f.write(received_data)
      #now3 = datetime.now()
      #f.write('%s'%now3)
      #f.write("\r\n")

      #f.close()
      print(received_data)
      time.sleep(1)

      c=NodeValue.ContentFromClient(received_data)
      c.sensorvalues()

      #print('here')
      host = socket.gethostbyname("103.37.200.35")
      s = socket.create_connection((host, 5000), 2)
      s.sendall(bytes(received_data,'utf-8'))
      print("data send")

      s.close()
    except Exception as e:
      ###print('exception is here')
      print(e,'')
      print('DATA CANT SEND')
      f = open('/home/sailab/ProjectCode/log.txt', 'a+')
      now1 = datetime.now()
      f.write(str(e))
      f.write(' ')
      f.write('%s'%now1)
      f.write("\r\n")
      f.close()
      ser = serial.Serial('/dev/ttyUSB0', 115200)
      connection=False
      if not connection:
        print('I AM TRYING TO CONNECT WIFI')
        f = open('/home/sailab/ProjectCode/log.txt', 'a+')
        if len(received_data)>10:
          now = datetime.now()
          f.write('%s'%now)
          f.write("\r\n")
          f.write(received_data)
          f.write("\r\n")
          f.close()
        received_data=""
        #connection=wire.connect(ssid='HUAWEI-9F29',password='Root@123')
        connection =wire.connect(ssid='HUAWEI-9F29',password='Root@123')
        print("Connected");





















'''
import sys
print('NEW DATA..................................')
#print(sys.version)
import time

import select
import socket
import json
#import httplib
import urllib
from datetime import datetime
#import NodeValue
#import Send_sms
import serial
ser = serial.Serial('/dev/ttyUSB0', 115200)
from wireless import Wireless
wire = Wireless()

try:
 status =wire.connect(ssid='HUAWEI_1B6B',password='Root@123')
 if status == True:
  print("NET IS PROPERLY CONNECTED")
 else:
  print("NET IS NOT CONNECTED")
except:
 print('ANY ISSUE IN NETWORKING')   #print('i have came here')
temp=''
while(True):
    try:

      ser.flush()
      time.sleep(1)

      print('waiting')
      received_data = ser.read() # Read the newest output
      #received_data = "&c1@netala@n2(moisture1:56.48)(voltage1:3.66)(vols1:2269.00)(pitch1:-85)(roll1:-12)(pitch2:24)(roll2:-68)(pitch3:86)(roll3:1)(pitch4:1)(roll4:84)!" # Read the newest output
      print(received_data)
      time.sleep(0.05)
      data_left = ser.inWaiting()
      received_data += ser.read(data_left)



      print(received_data,'is received from Sensor')
      index_strt=received_data.find('&')
      index_end=received_data.find('!')
      if(index_end!=-1 and index_strt!=-1):
        temp=''
      if(index_end==-1 and index_strt==-1):
        temp=''
        continue
      if(index_end!=-1 and index_strt>index_end):
        temp=''
        continue;
      if(index_end==-1):
        temp=received_data
        continue;#
        #print('i am in loop2')
        #print (received_Data)
      received_data=temp+received_data
      temp=''
      received_data=received_data[index_strt+1:index_end]
      f=open('/home/pi/Desktop/latest/All.txt','a+')
      f.write(received_data)
      now3 = datetime.now()
      f.write('%s'%now3)
      f.write("\r\n")

      f.close()
      print(received_data)
      time.sleep(1)
      #received_data='hi'

      #c=NodeValue.ContentFromClient(received_data)
      #c.sensorvalues()


      host = socket.gethostbyname("103.37.200.16")
      s = socket.create_connection((host, 5000), 2)
      s.sendall(received_data)
      print("data send")

      s.close()
    except Exception as e:
      print(e,'')
      print('DATA CANT SEND')
      f = open("/home/pi/Desktop/latest/error.txt", "a+")
      now1 = datetime.now()
      f.write(str(e))
      f.write(' ')
      f.write('%s'%now1)
      f.write("\r\n")
      f.close()
      connection=False
      if not connection:
        print('I AM TRYING TO CONNECT WIFI')
        f = open("/home/pi/Desktop/latest/LOG.txt", "a+")
        if len(received_data)>10:
          now = datetime.now()
          f.write('%s'%now)
          f.write("\r\n")
          f.write(received_data)
          f.write("\r\n")
          f.close()
        received_data=""
        connection=wire.connect(ssid='HUAWEI-9F29',password='Root@123')

        print("Connected");



#New code : date - 10 Apr 2025
#!/usr/bin/python3

import time
import os
import socket
import json
from datetime import datetime
import NodeValue
import serial
import subprocess

# Function to check if internet is connected
def internet_connected():
    try:
        subprocess.check_call(["ping", "-c", "1", "8.8.8.8"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# Initialize serial connection
s = True
global ser
global received_data

# Wait until serial device is connected
while s:
    try:
        # Open serial port
        ser = serial.Serial('/dev/ttyUSB0', 115200)
        print('Connected to serial port')
        s = False
    except Exception as e:
        print(f'NOT CONNECTED TO SL, {e}')
        s = True
        time.sleep(1)

# Check if internet is available via the Huawei dongle
if internet_connected():
    print("Internet is already connected via the dongle")
else:
    print("No internet connection. Please check the dongle.")

# Main loop to read data from serial and send it to the server
while True:
    try:
        print('Waiting on serial...')
        ser.flush()
        time.sleep(1)

        # Read data from serial port
        data = ser.read()  # Read the newest output
        print(data)
        time.sleep(0.05)

        # Read remaining data if available
        data_left = ser.inWaiting()
        data += ser.read(data_left)

        # Decode the received data
        received_data = data.decode()

        # Parse the received data to extract relevant information
        index_strt = received_data.find('&')
        index_end = received_data.find('!')

        # If the data is malformed, skip
        if index_end == -1 or index_strt == -1 or received_data.count('@') != 2 or received_data[-1] != '!' or received_data.count('!') != 1 or received_data.count('&') != 1:
            continue

        # Extract valid data between the start and end markers
        received_data = received_data[index_strt + 1:index_end]

        # Write the data to a file for logging
        with open('/home/pi/Desktop/latest/All.txt', 'a+') as f:
            f.write(received_data)
            now3 = datetime.now()
            f.write(f'{now3}\r\n')

        print(received_data)
        time.sleep(1)

        # Process the data (assuming you have logic in NodeValue)
        c = NodeValue.ContentFromClient(received_data)
        c.sensorvalues()

        # Send the data to a remote server via socket
        host = socket.gethostbyname("103.37.200.35")
        s = socket.create_connection((host, 5000), 2)
        s.sendall(bytes(received_data, 'utf-8'))
        print("Data sent")

        s.close()

    except Exception as e:
        # Handle exceptions and log errors
        print(f"Error: {e}")
        print('DATA CANNOT BE SENT')
        with open('/home/pi/Desktop/latest/error1.txt', 'a+') as f:
            now1 = datetime.now()
            f.write(f'{e} {now1}\r\n')

        # Attempt to reconnect the serial port if there's an issue
        try:
            ser = serial.Serial('/dev/ttyUSB0', 115200)
        except Exception as reconnect_error:
            print(f"Reconnection failed: {reconnect_error}")

        # Check if internet connection is available, otherwise try to reconnect
        if not internet_connected():
            print("Attempting to reconnect to the dongle...")
            # Optionally log the received data before attempting a reconnect
            with open('/home/pi/Desktop/latest/LOG.txt', 'a+') as f:
                if len(received_data) > 10:
                    now = datetime.now()
                    f.write(f'{now}\r\n{received_data}\r\n')

            received_data = ""
            # Skip the WiFi connection attempt, as the dongle is already providing internet.
            print("Internet is available via the dongle")

        time.sleep(1)
'''
