#!/usr/bin/python

# DHT22 sensor Module

import time, sys, socket
import Adafruit_DHT
from datetime import datetime

# gpio pin used by the sensor
gpio=18

modulename=sys.argv[2]
modulitem="internal_thermometer"
memdb_port=int(sys.argv[1])

def DBSendText(text):
#    print(text)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', memdb_port))
#    s.send(text)
    s.send(text.encode())

    data = s.recv(1024)
#    print(data)
    s.close()
    return data.strip()

#main loop
while True:
    #get the value of the sensor                  v-- Using DHT22 here
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, gpio)
    #send to the server
    if not isinstance(temperature, float) or float(temperature) < 5.0:
        print('ERROR:'+ datetime.now().strftime("%H:%M:%S"))
#        time.sleep(20)
    else:
        humidity="{:.2f}".format(humidity)
        temperature="{:.2f}".format(temperature)

#        print(humidity, temperature)
        data=DBSendText('S VALUES '+modulename+' '+modulitem+'_humidity '+humidity)
        data=DBSendText('S VALUES '+modulename+' '+modulitem+'_temperature '+temperature)
        time.sleep(60)
