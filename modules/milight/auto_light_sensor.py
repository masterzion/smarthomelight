#!/usr/bin/python
import os, sys, milight, time, datetime, socket

gpioID = 23
min_lumens = 5


#if len(sys.argv) < 3:
#    print "Usage:"
#    print sys.argv[0] + " $LOCKFILE $MILIGHT_IP $MILIGHT_PORT $MILIGHT_GROUP "
#    sys.exit(2)


#get param 
lock_file     = sys.argv[1]
milight_ip    = sys.argv[2]
milight_port  = int(sys.argv[3])
milight_group = int(sys.argv[4])

SUNSET_RANGE = range(11,22)

get_lumens_string='G VALUES light_sensor internal_light_sensor'
get_houseisempty_string='G VALUES houseisempty mobile_check'



#connect to milight 
print lock_file + " " +  milight_ip + " " + str(milight_port) + " " + str(milight_group)
controller = milight.MiLight({'host': milight_ip, 'port': milight_port}, wait_duration=0)
light = milight.LightBulb(['rgbw']) # Can specify which types of bulbs to use
last_mobile_status = True

def getlumens( s ):
   s.send(get_lumens_string)
   data = s.recv(1024)
#   print data
   return float(data)

def houseisempty( s ):
   s.send(get_houseisempty_string)
   data = s.recv(1024)
#   print data
   return bool(data == "0")

#connect to the memory db
port=int(sys.argv[1])
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))



# main loop
while True:
    time.sleep(60)
    TIMENOW=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())+" "

    mobile_status = houseisempty( s )
    lumens = getlumens(s)
#    print mobile_status
    
    if mobile_status != last_mobile_status:
        if mobile_status:
#            print TIMENOW+"light sensor: " + str(lumens)
            if (lumens < min_lumens) :
#                print "set light on"
                time.sleep(4)
                controller.send(light.fade_up(milight_group))
#                light.wait(0)
                last_mobile_status = mobile_status
        else:       
          controller.send(light.off(milight_group)) 
#          print TIMENOW+"set light Off"
          last_mobile_status = mobile_status

#    if (lumens > min_lumens) :
#      print TIMENOW+"set light Off (lumens)"
#      controller.send(light.off(milight_group)) 
#      time.sleep(30)
#     controller.send(light.all_off()) # Turn off all lights
    if ( not houseisempty( s ) ) and mobile_status and (lumens < min_lumens):
        date = datetime.datetime.today()
        if date.hour in SUNSET_RANGE:
#           print TIMENOW+"set light on (Sunset)"
           controller.send(light.fade_up(milight_group))
