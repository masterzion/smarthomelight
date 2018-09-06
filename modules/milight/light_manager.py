#!/usr/bin/python
import os, sys, milight, socket, time

memdb_host = 'localhost'
memdb_port=int(sys.argv[1])
modulename=sys.argv[2]

milight_ip    = sys.argv[3]
milight_port  = int(sys.argv[4])

modulitem='light_manager'

#connect to milight 
controller = milight.MiLight({'host': milight_ip, 'port': milight_port}, wait_duration=0)
light = milight.LightBulb(['rgbw']) # Can specify which types of bulbs to use

#Turn off all lights
controller.send(light.all_off())

status="0,0,0,0"
last_status=status

def getgroup(group):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((memdb_host, memdb_port))
    s.send('G PIDS '+modulename+' '+'switch_group'+str(group))
    data = s.recv(1024)
    if data in ["0", ""]:
        return "0"
    else:
        return "1"

# main loop
while True:
    #get the answer
    status = getgroup(1)+','+getgroup(2)+','+getgroup(3)+','+getgroup(4)
#    print status
    
    if not status == last_status :
        for group in [0,1,2,3] :
            ar_status = status.split(',')
            ar_last_status = last_status.split(',')
            if not ar_last_status[group] == ar_status[group]:
#                print "group "+str(group) + ": "+ ar_status[group]
                migroup=int(group)+1
                if ar_status[group] == '1' :
                    controller.send(light.fade_up(migroup))
                    time.sleep(2)
                    controller.send(light.white(migroup))
                else:
                    controller.send(light.fade_down(migroup))
                    time.sleep(2)
                    controller.send(light.off(migroup))

    last_status = status
    time.sleep(1)

