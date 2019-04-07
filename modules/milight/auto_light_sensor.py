#!/usr/bin/python
import os, sys,  time, datetime, socket

min_lumens = 20
max_lumens = 25
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

last_light_status = "00"

last_mobile_status = False

port=int(sys.argv[1])
host = 'localhost'


def sendtext(text):
    #connect to the memory db
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
#    print text
    s.send(text)
    data = s.recv(1024)
    s.close()
#    print data
    return data

def setmilight(val, group = "1"):
    global last_light_status
    if val == last_light_status:
        return "none"
    else:
#        print 'S PIDS '+modulename+' '+'switch_group'+group+' '+val
        data = sendtext('S PIDS '+modulename+' '+'switch_group'+group+' '+val)
        last_light_status = val
        return data

def getlumens():
    data = sendtext(get_lumens_string)
    return float(data)

def houseisempty():
    data = sendtext(get_houseisempty_string)
    if data == "":
        data = "0"
    return bool(data == "0")


setmilight("0")
time.sleep(3)

# main loop
while True:
    TIMENOW=time.strftime("%H:%M:%S", time.gmtime())

    if TIMENOW in ["12:00:00","12:00:01","12:00:02","12:00:03","12:00:04","12:00:05"]:
       last_mobile_status = False

    TIMENOW=TIMENOW+" "
    lumens = getlumens()
#    print TIMENOW+"light sensor: " + str(lumens)
    if lumens > max_lumens:
        setmilight("0", "1")
        setmilight("0", "2")
        setmilight("0", "3")
        setmilight("0", "4")
        last_mobile_status = False
    else:
        mobile_status = houseisempty()
    #    print last_mobile_status
    #    print mobile_status
        if mobile_status != last_mobile_status:
            if mobile_status:
                if (lumens < min_lumens) :
    #                print "set light on"
                    setmilight("-1")
                    last_mobile_status = mobile_status
            else:
              setmilight("0")
    #          print TIMENOW+"set light Off"
              last_mobile_status = mobile_status

        if ( not houseisempty() ) and mobile_status and (lumens < min_lumens):
            date = datetime.datetime.today()
            if date.hour in SUNSET_RANGE:
    #           print TIMENOW+"set light on (Sunset)"
               setmilight("-1")
    time.sleep(3)
