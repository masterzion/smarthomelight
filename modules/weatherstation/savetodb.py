#!/usr/bin/python

import os,time,sys,socket

from time import gmtime, strftime
from models import Sensors

memdb_host = 'localhost'
memdb_port=int(sys.argv[1])


maxtry=5

def DBSendText(text):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((memdb_host, memdb_port))
    s.send(text)
    data = s.recv(1024)
#    print text+ ':'+data
    s.close()
    return data.strip()


def savetodb(num):
    try:
        datetime=strftime("%d-%m-%Y %H:%M", time.localtime())

        sensor1_value   = DBSendText('G VALUES thermometer external_thermometer')
        time.sleep(1)
        sensor2_value_h = DBSendText('G VALUES thermometer internal_thermometer_humidity')
        time.sleep(1)
        sensor2_value_t = DBSendText('G VALUES thermometer internal_thermometer_temperature') 
        time.sleep(1)
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
    time.sleep(50)
