#!/usr/bin/python3

import time, sys, socket
import adafruit_dht
from datetime import datetime

gpio_dht=18 # sensor
dhtDevice = adafruit_dht.DHT22(gpio_dht)

modulename=sys.argv[2]
modulitem="internal_thermometer"
memdb_port=int(sys.argv[1])

time.sleep(3)

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
    time.sleep(15)
    try:
      humidity = dhtDevice.humidity
      data=DBSendText('S VALUES '+modulename+' '+modulitem+'_humidity '+str(humidity))
      time.sleep(30)
      temperature = dhtDevice.temperature
      if temperature > 5:
 #       print(humidity, temperature)
         data=DBSendText('S VALUES '+modulename+' '+modulitem+'_temperature '+str(temperature))
      time.sleep(10)
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    time.sleep(5)
