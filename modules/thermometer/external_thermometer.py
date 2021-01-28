#!/usr/bin/python

# DHT22 sensor Module

import time, sys, socket, os
from w1thermsensor import W1ThermSensor

modulename=sys.argv[2]
modulitem="external_thermometer"


# init sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
sensor = W1ThermSensor()

#connect to the memory db
port=int(sys.argv[1])
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))


#main loop
while True:
    value =  sensor.get_temperature()
    time.sleep(2)
    value = str ( (sensor.get_temperature()+value) /2 )

    #print(value)
    #send to the server
    s.send('S VALUES '+modulename+' '+modulitem+' '+value)
    #get the answer
    data = s.recv(1024)
    #print data

    #wait
    time.sleep(60)
