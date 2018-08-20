#!/usr/bin/python

import os,time,sys,socket

from time import gmtime, strftime
from models import Sensors

memdb_host = 'localhost'
memdb_port=int(sys.argv[1])

#connect to the memory db
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((memdb_host, memdb_port))

maxtry=5




def savetodb(num):
    try:
        datetime=strftime("%d-%m-%Y %H:%M", time.localtime())

        s.send('G VALUES thermometer external_thermometer')
        sensor1_value = s.recv(1024)

        s.send('G VALUES thermometer internal_thermometer_humidity')
        sensor2_value_h=s.recv(1024)

        s.send('G VALUES thermometer internal_thermometer_temperature')
        sensor2_value_t = s.recv(1024)

#        print sensor1_value,sensor2_value_t, sensor2_value_h, datetime

        Sensors().InsertData(sensor1_value,sensor2_value_t, sensor2_value_h, datetime)
        return True
    except ValueError:
      if num < maxtry:
         time.sleep(30)
         print ValueError
         return savetodb(num+1)
      else:
         return False

while savetodb(1):
    time.sleep(60)

