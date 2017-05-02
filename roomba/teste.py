
import datetime, time
import RPi.GPIO as GPIO 

gpioID = 21


#set relay config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioID, GPIO.OUT)


def sendOne():
    GPIO.output(gpioID, GPIO.HIGH)
    print "1"


def sendZero():
    GPIO.output(gpioID, GPIO.LOW)
    print "0"




while True:

    GPIO.output(gpioID, GPIO.LOW)
    time.sleep(1)
    sendZero()

    time.sleep(1)
    sendOne()
