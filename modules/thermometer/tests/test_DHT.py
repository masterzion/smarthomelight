#!/usr/bin/python
import time
import Adafruit_DHT
from datetime import datetime

dhtpin=18


while True:
    sensor2_value_h, sensor2_value_t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, dhtpin)
    if isinstance(sensor2_value_t, float):
      print sensor2_value_h, sensor2_value_t
    else:
      current_time = now.strftime("%H:%M:%S")
      print("Error: ", current_time)
    time.sleep(2)
