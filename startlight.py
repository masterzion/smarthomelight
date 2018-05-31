#!/usr/bin/python
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

import os, sys, milight, time, smbus

from time import gmtime, strftime

gpioID = 23
min_lumens = 4

#set relay config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioID, GPIO.OUT)


#if len(sys.argv) < 3:
#    print "Usage:"
#    print sys.argv[0] + " $LOCKFILE $MILIGHT_IP $MILIGHT_PORT $MILIGHT_GROUP "
#    sys.exit(2)

#get param 
lock_file     = sys.argv[1]
milight_ip    = sys.argv[2]
milight_port  = int(sys.argv[3])
milight_group = int(sys.argv[4])

#light senso params
DEVICE     = 0x23 # Default device I2C address
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value
CONTINUOUS_LOW_RES_MODE = 0x13
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
ONE_TIME_LOW_RES_MODE = 0x23
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
 
#light sensor funcs
def convertToNumber(data):
  return ((data[1] + (256 * data[0])) / 1.2)

def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)


#connect to milight 
print lock_file + " " +  milight_ip + " " + str(milight_port) + " " + str(milight_group)
controller = milight.MiLight({'host': milight_ip, 'port': milight_port}, wait_duration=0)
light = milight.LightBulb(['rgbw']) # Can specify which types of bulbs to use
last_mobile_status = True

# main loop
while True:
    print strftime("%Y-%m-%d %H:%M:%S", gmtime())
    # check if the mobile is out of the network 3 times
    mobile_status = not os.path.isfile(lock_file) 
    print "mobile status " +  str(mobile_status)
    print "last mobile status " + str(last_mobile_status)

    if mobile_status != last_mobile_status:
        if mobile_status:
            GPIO.output(gpioID, GPIO.LOW) #music box power On
            lumens = int(readLight())

            print "light sensor: " + str(lumens)
            if (lumens < min_lumens) :
                print "set light and music On"
                time.sleep(4)
                controller.send(light.fade_up(milight_group))
                light.wait(0)
                last_mobile_status = mobile_status
        else:       
          #controller.send(light.off(1)) # Turn off group 1 lights
          controller.send(light.all_off()) # Turn off all lights, equivalent to light.off(0)
          print "set light and music Off"
          GPIO.output(gpioID, GPIO.HIGH) #music box power Off
          last_mobile_status = mobile_status

    time.sleep(2)
    lumens = int(readLight())
    if (lumens > min_lumens) :
      controller.send(light.all_off()) # Turn off all lights
      print "set light Off"
