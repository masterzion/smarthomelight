#!/usr/bin/python
import datetime, time, socket, sys

gpioID = 24

lastStatus = 99
setEnable = True

modulename=sys.argv[2]
item_name='fan_turnon'

turnon_temperature_range = range(25,40)

#connect to the memory db
port=int(sys.argv[1])
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

get_internal_thermometer_string='G VALUES thermometer internal_thermometer_temperature'
get_houseisempty_string='G VALUES houseisempty mobile_check'
get_mintemp_string='G VALUES fan auto_fan_sensibility'
set_mintemp_string='S VALUES fan auto_fan_sensibility '



def getmintemp( s ):
   s.send(get_mintemp_string)
   data =  s.recv(1024)
#   print "temp_sensibility:" + data
   val= (100-int(data)) / 20
   val = val+22
#   print("temp:"+str(val))
   return val



def setmintemp( s, temp ):
   s.send(set_mintemp_string+str(temp))
   data =  s.recv(1024)
#   print "settempres:" + data + str(temp)
   return data




def gethouseisempty( s ):
   s.send(get_houseisempty_string)
   data = s.recv(1024)
#   print data
   return (data == "1")

def gettemperature( s ):
   s.send(get_internal_thermometer_string)
   data =  s.recv(1024)
#   print "temperature:" + data
   return int(float(data))


silenthours = range(0,9)
workinghours = range(16,18)

setmintemp(s, 40)
time.sleep(1)
mintemp=getmintemp(s)
time.sleep(1)

while True:
    setEnable = False
    date = datetime.datetime.today()
    houseisempty = gethouseisempty(s)
    turnon_temperature_range = range(mintemp, 40)

    if houseisempty:
#        print "is empty"
        if not date.weekday() in [5,6]:
            if date.hour in workinghours:
                internal_temp=gettemperature(s)
                if internal_temp in turnon_temperature_range:
                    setEnable = True
    else:
#        print  date.hour 
        if date.hour not in silenthours:
            internal_temp=gettemperature(s)
#            print internal_temp
            if internal_temp in turnon_temperature_range:
                setEnable = True


#    print setEnable
    if setEnable != lastStatus :
#        print "different"
        if setEnable:
            s.send('S PIDS '+modulename+' '+item_name+' -1')
            data = s.recv(1024)
        else:
            s.send('S PIDS '+modulename+' '+item_name+' 0')
            data = s.recv(1024)
        lastStatus = setEnable
    for n in range(10):
       time.sleep(60)
       newtemp=getmintemp(s)
       if not newtemp == mintemp:
          mintemp=newtemp
          break


