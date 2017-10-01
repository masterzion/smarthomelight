#!/usr/bin/python


try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

import pyping, sys, milight, time, smbus


gpioID = 23


#set relay config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioID, GPIO.OUT)



#if len(sys.argv) < 3:
#    print "Usage:"
#    print sys.argv[0] + " $MOBILE_IP $MILIGHT_IP $MILIGHT_PORT $MILIGHT_GROUP "
#    sys.exit(2)

#get param 
mobile_ip     = sys.argv[1]
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
print mobile_ip + " " +  milight_ip + " " + str(milight_port) + " " + str(milight_group)
controller = milight.MiLight({'host': milight_ip, 'port': milight_port}, wait_duration=0)
light = milight.LightBulb(['rgbw']) # Can specify which types of bulbs to use
last_mobile_status = False

# main loop
while True:
    # check if the mobile is out of the network 3 times
    count=0
    while True:
        if count > 90:
            break
        r = pyping.ping(mobile_ip)
        mobile_status = (r.ret_code == 0)
        print str(count) + " Mobile:" + str(mobile_status)
        if mobile_status:
            break
        else:
            count += 1
            time.sleep(1)

    if mobile_status != last_mobile_status:
        if mobile_status:
            GPIO.output(gpioID, GPIO.LOW) #relay On
            lumens = int(readLight())
            for x in range(0, 3):
                time.sleep(1)
                lumens += int(readLight())

            print "light sensor: " + str(lumens)
            if (lumens == 0.0) :
                print "set On"
                time.sleep(4)
                controller.send(light.fade_up(milight_group))
                light.wait(0)
                last_mobile_status = mobile_status
        else:
          #controller.send(light.fade_down(milight_group))
          #controller.send(light.off(1)) # Turn off group 1 lights
          controller.send(light.all_off()) # Turn off all lights, equivalent to light.off(0)
          print "set Off"
          GPIO.output(gpioID, GPIO.HIGH) #relay Off
          last_mobile_status = mobile_status

    time.sleep(2)

