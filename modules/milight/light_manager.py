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
color='ff8800,ff8800,ff8800,ff8800'
last_status=status
last_color=color

def getgroup(group):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((memdb_host, memdb_port))
    s.send('G PIDS '+modulename+' '+'switch_group'+str(group))
    data = s.recv(1024)
    if data in ["0", ""]:
        return "0"
    else:
        return "1"

def getcolor(group):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((memdb_host, memdb_port))
    str_conn='G VALUES '+modulename+' '+'switch_group'+str(group)
    s.send(str_conn)
    data = s.recv(1024)
#    print str_conn+" = "+data
    if data in ["ffffff", ""]:
        return "ffffff"
    else:
        return data



# main loop
while True:
    #get the answer
    status = getgroup(1)+','+getgroup(2)+','+getgroup(3)+','+getgroup(4)
    color = getcolor(1)+','+getcolor(2)+','+getcolor(3)+','+getcolor(4)
#    print status
#    print color
    
    if not (status == last_status and color == last_color):
        for group in [0,1,2,3] :
            ar_status = status.split(',')
            ar_color = color.split(',')
            ar_last_status = last_status.split(',')
            ar_last_color  = last_color.split(',')
            if not (ar_last_status[group] == ar_status[group] and ar_last_color[group] == ar_color[group]):
#                print "group "+str(group) + " - status "+ ar_status[group] +" - color " +ar_color[group]
                migroup=int(group)+1
                if ar_status[group] == '1' :
#                    print "on"
                    controller.send(light.brightness(0, migroup))
                    time.sleep(0.2)
                    controller.send(light.color(milight.color_from_hex('#'+ar_color[group]), migroup))
                    time.sleep(0.5)
                    controller.send(light.fade_up(migroup))
                    controller.send(light.brightness(100, migroup))
                else:
                    if not (ar_last_status[group] == ar_status[group]):
#                      print "off"
                      controller.send(light.fade_down(migroup))
                      time.sleep(0.5)
                      controller.send(light.fade_down(migroup))
                      time.sleep(4)
                      for force_off in [0,1,2,3] :
                         time.sleep(1.5)
                         controller.send(light.off(migroup))
#                print "sleep"
                time.sleep(2)

    last_status = status
    last_color = color
    time.sleep(2)
