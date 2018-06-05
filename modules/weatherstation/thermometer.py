#!/usr/bin/python

import os

import time
import Adafruit_DHT

from time import gmtime, strftime

from models import Sensors


dhtpin=18
 
 


while True:
    #
    sensor2_value_h, sensor2_value_t = 
    print sensor2_value_h, sensor2_value_t

    if sensor2_value_t  and sensor2_value_h:      
       #
       sensor1_value = 
       
       datetime=strftime("%d-%m-%Y %H:%M", time.localtime())
       print sensor1_value
       if sensor1_value < 41 :
          Sensors().InsertData(sensor1_value,sensor2_value_t, sensor2_value_h, datetime)
          print sensor1_value,sensor2_value_t, sensor2_value_h, datetime
       time.sleep(60)
    else:
       time.sleep(5)
