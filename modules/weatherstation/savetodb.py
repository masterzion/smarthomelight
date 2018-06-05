#!/usr/bin/python

import os,time,sys,socket

from time import gmtime, strftime
from models import Sensors

memdb_host = 'localhost'
memdb_port=int(sys.argv[1])

#connect to the memory db
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((memdb_host, memdb_port))


while True:
    datetime=strftime("%d-%m-%Y %H:%M", time.localtime())

    s.send('G VALUES thermometer external_thermometer')
    sensor1_value = s.recv(1024)
    
    s.send('G VALUES thermometer internal_thermometer')
    sensor2_value_h, sensor2_value_t = s.recv(1024).split(',')
    
#    print sensor1_value,sensor2_value_t, sensor2_value_h, datetime

    Sensors().InsertData(sensor1_value,sensor2_value_t, sensor2_value_h, datetime)
    time.sleep(60)

