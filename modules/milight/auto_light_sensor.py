#!/usr/bin/python
import os, sys,  time, datetime, socket

gpioID = 23
min_lumens = 5


#if len(sys.argv) < 3:
#    print "Usage:"
#    print sys.argv[0] + " $LOCKFILE $MILIGHT_IP $MILIGHT_PORT $MILIGHT_GROUP "
#    sys.exit(2)


#get param 


SUNSET_RANGE = range(11,22)

modulename=sys.argv[2]


get_lumens_string='G VALUES light_sensor internal_light_sensor'
get_houseisempty_string='G VALUES houseisempty mobile_check'

milight_string=' VALUES '+modulename+' light_manager'

#connect to milight 
last_mobile_status = False


def setmilight( s , val):
#   print "setmilight: "+'G' + milight_string
   s.send('G' + milight_string)
   data = s.recv(1024)
#   print data
   if data == "":
     data = '1,0,0,0'
   
   data =  val+data[1:]
#   print data   
   s.send('S' + milight_string +' '+  data)
   data = s.recv(1024)
#   print data
   return data




def getlumens( s ):
   s.send(get_lumens_string)
   data = s.recv(1024)
#   print data
   return float(data)


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
    TIMENOW=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())+" "

    mobile_status = houseisempty( s )
    lumens = getlumens(s)
#    print mobile_status


    if mobile_status != last_mobile_status:
        if mobile_status:
#            print TIMENOW+"light sensor: " + str(lumens)
            if (lumens < min_lumens) :
#                print "set light on"
                setmilight(s, "1")
                last_mobile_status = mobile_status
        else:       
          setmilight(s, "0")
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
           setmilight(s, "1")
    time.sleep(60)