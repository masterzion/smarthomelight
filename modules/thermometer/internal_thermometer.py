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
    #get the value of the sensor                                             v-- Using DHT22 here
    sensor2_value_h, sensor2_value_t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, gpio)
    value=str(sensor2_value_h)+','+str(sensor2_value_t)
    #print value
    
    #send to the server
    s.send('S VALUES '+modulename+' '+modulitem+' '+value)
    
    #get the answer
    data = s.recv(1024)
    #print data

    #wait
    time.sleep(60)
