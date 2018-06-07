#!/usr/bin/python
import datetime, time, socket, sys

min_temp = 21.5
max_temp = 23
gpioID = 24


lastStatus = True
setEnable = False

modulename=sys.argv[2]
item_name='heater_on'

#connect to the memory db
port=int(sys.argv[1])
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

get_internal_thermometer_string='G VALUES thermometer internal_thermometer'


def getInternalThermometer( s ):
   s.send(get_internal_thermometer_string)
   data =  s.recv(1024).split(',')[1]
   print data
   return float(data)


while True:
  date = datetime.datetime.today()

  #turn off during the night
  silenthours = range(0,11)
  silenthours = silenthours + range(20,23)

  if date.weekday() not in [5,6]:
     silenthours = silenthours + range(11,13)
#  print silenthours

#  print date
  if date.hour not in silenthours:
     internal_temp = getInternalThermometer( s );
     
     if setEnable:
         if internal_temp > max_temp-1:
            setEnable = False
     else:
         if internal_temp < min_temp:
            setEnable = True
  else:
     setEnable = False
#     print "offline time"

  print setEnable
  if setEnable != lastStatus :
     if setEnable:
        s.send('S PIDS '+modulename+' '+item_name+' 1')
        data = s.recv(1024)
     else:
        s.send('S PIDS '+modulename+' '+item_name+' 0')
        data = s.recv(1024)
     lastStatus = setEnable

  time.sleep(60 * 5)