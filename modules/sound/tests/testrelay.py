import RPi.GPIO as GPIO
import time

id=17
ntime=2
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(id,GPIO.OUT)
while True:
  print "LED on"
  GPIO.output(id,GPIO.HIGH)
  time.sleep(ntime)
  print "LED off"
  GPIO.output(id,GPIO.LOW)
  time.sleep(ntime)


