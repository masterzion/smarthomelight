
import datetime, time
import RPi.GPIO as GPIO 

#gpioID = 27
gpioID = 17

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
    time.sleep(5)
    sendZero()

    time.sleep(5)
    sendOne()
