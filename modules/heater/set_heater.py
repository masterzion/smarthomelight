#!/usr/bin/python
import os, sys, socket, time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

def sendtext(text):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', memdb_port))
    s.send(text)
    data = s.recv(1024)
#    print text+ ':'+data
    s.close()
    return data.strip()

memdb_host = 'localhost'
memdb_port=int(sys.argv[1])
modulename=sys.argv[2]
moduleitem="heater_turnon"

gpio=26

gpio_value=0
GPIO.setmode(GPIO.BCM)

GPIO.setup(gpio, GPIO.OUT, initial=GPIO.LOW)
sendtext('S VALUES '+modulename+' '+moduleitem+' 0')

while True:
    value=sendtext('G PIDS '+modulename+' '+moduleitem)
   

    if value == "":
       value="0"

    if value == "0":
       GPIO.output(gpio, GPIO.HIGH) 
    else:
       GPIO.output(gpio, GPIO.LOW) 

    
    time.sleep(5)
