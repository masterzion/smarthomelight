#!/usr/bin/python
import datetime, time, socket, sys



gpioID = 24


lastStatus = 99
setEnable = True

modulename=sys.argv[2]
item_name='fan_turnon'

turnon_temperature_range = range(25,35)

#connect to the memory db
port=int(sys.argv[1])
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

get_internal_thermometer_string='G VALUES thermometer internal_thermometer_temperature'
get_houseisempty_string='G VALUES houseisempty mobile_check'

def gethouseisempty( s ):
   s.send(get_houseisempty_string)
   data = s.recv(1024)
#   print data
   return bool(data == "0")

def gettemperature( s ):
   s.send(get_internal_thermometer_string)
   data =  s.recv(1024).split(',')[1]
#   print data
   return int(float(data))


silenthours = range(0,11)
silenthours = silenthours + range(20,23)
workinghours = range(16,18)


while True:
    time.sleep(20 * 60)

    setEnable = False
    date = datetime.datetime.today()
    houseisempty = gethouseisempty(s)

    if houseisempty:
        if not date.weekday() in [5,6]:
            if date.hour in workinghours:
                internal_temp=gettemperature(s)
                if internal_temp in turnon_temperature_range:
                    setEnable = True
    else:
        if date.hour not in silenthours:
            internal_temp=gettemperature(s)
#            print internal_temp
            if internal_temp in turnon_temperature_range:
                setEnable = True


#    print setEnable
    if setEnable != lastStatus :
#        print "different"
        if setEnable:
            s.send('S PIDS '+modulename+' '+item_name+' 1')
            data = s.recv(1024)
        else:
            s.send('S PIDS '+modulename+' '+item_name+' 0')
            data = s.recv(1024)
        lastStatus = setEnable
