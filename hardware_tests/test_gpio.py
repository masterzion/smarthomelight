#!/usr/bin/python
import datetime, time, sys

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

if len(sys.argv) == 1:
   print("Usage:\n ./"+sys.argv[0]+" [gpio_port]")
   sys.exit()
else:
   gpioID = int(sys.argv[1])



 
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioID, GPIO.OUT)


while True:
    time.sleep(1)
    print("off")
    GPIO.setup(gpioID, GPIO.OUT)
    time.sleep(1)
    print("on")
    GPIO.output(gpioID, GPIO.HIGH)

