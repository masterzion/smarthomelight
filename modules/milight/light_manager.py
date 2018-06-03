#!/usr/bin/python
import os, sys, milight, socket

milight_ip    = sys.argv[1]
milight_port  = int(sys.argv[2])

milight_group = 1

#connect to milight 
controller = milight.MiLight({'host': milight_ip, 'port': milight_port}, wait_duration=0)
light = milight.LightBulb(['rgbw']) # Can specify which types of bulbs to use

last_status=["1","1","1","1"]
status = ["0","0","0","0"]


# main loop
while True:
    controller.send(light.fade_up(milight_group))
