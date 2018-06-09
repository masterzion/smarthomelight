#!/usr/bin/python

# DHT22 sensor Module

import time, sys, socket
import Adafruit_DHT

# gpio pin used by the sensor
gpio=18

modulename=sys.argv[2]
modulitem="internal_thermometer"


#connect to the memory db
port=int(sys.argv[1])
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

#main loop
while True:
    #get the value of the sensor                  v-- Using DHT22 here
    data = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, gpio)

    #print data
    
    #send to the server
    humidity=str(data[0])
    temperature=str(data[1])
    s.send('S VALUES '+modulename+' '+modulitem+'_humidity '+humidity)
    data = s.recv(1024)
        
    s.send('S VALUES '+modulename+' '+modulitem+'_temperature '+temperature)
    data = s.recv(1024)

    #wait
    time.sleep(60)