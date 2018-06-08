#!/usr/bin/python
import  sys, milight, time


if len(sys.argv) == 1:
  print "Usage:"
  print " "+sys.argv[0] + " IP " + "PORT"
  print "Example:"
  print " "+sys.argv[0] + " 192.168.0.10 " + "8899"
  sys.exit()

else:
  milight_ip    = sys.argv[1]
  milight_port  = int(sys.argv[2])

  

controller = milight.MiLight({'host': '192.168.0.5', 'port': 8899}, wait_duration=0) #Create a controller with 0 wait between commands
light = milight.LightBulb(['rgbw', 'white', 'rgb']) #Can specify which types of bulbs to use



while True:
    controller.send(light.all_off())
    time.sleep(5)
    controller.send(light.all_on()) 
    time.sleep(5)