#!/usr/bin/python3

# DHT22 sensor Module

import time, sys, socket
import adafruit_dht
from datetime import datetime

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")


gpio_dht=18 # sensor
gpio_relay=26 # relay

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_relay, GPIO.OUT, initial=GPIO.HIGH)


dhtDevice = adafruit_dht.DHT22(gpio_dht)

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
    humidity = dhtDevice.humidity
    temperature = dhtDevice.temperature
    if temperature > 5:
#     print(humidity, temperature)
      data=DBSendText('S VALUES '+modulename+' '+modulitem+'_humidity '+str(humidity))
      data=DBSendText('S VALUES '+modulename+' '+modulitem+'_temperature '+str(temperature))
      time.sleep(60)
    else:
      time.sleep(1)
