#!/usr/bin/python
import datetime, time, socket, sys

lastStatus = 99
setEnable = True

modulename=sys.argv[2]
item_name='fan_turnon'

const_temp = 29

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
#   print("temp_sensibility:" + data)
   return int(data)

def setmintemp( s, temp ):
   s.send(set_mintemp_string+str(temp))
   data =  s.recv(1024)
#   print("settempres:" + data + str(temp))
   return data

def gethouseisempty( s ):
   s.send(get_houseisempty_string)
   data = s.recv(1024)
#   print(data)
   return (data == "1")

def gettemperature( s ):
   s.send(get_internal_thermometer_string)
   data =  s.recv(1024)
#   print("temperature:" + data)
   return int(float(data))


silenthours = range(0,9)
workinghours = range(16,18)

setmintemp(s, 10)
time.sleep(1)

while True:
    setEnable = False
    internal_temp=gettemperature(s)
    time.sleep(1)
    target_temp=const_temp-(getmintemp(s)/10)

#    print("target_temp: " + str(target_temp) )
    time.sleep(1)
    date = datetime.datetime.today()
    houseisempty = gethouseisempty(s)

    if houseisempty:
#        print("is empty")
        if not date.weekday() in [5,6]:
            if date.hour in workinghours:
                if internal_temp > target_temp:
                    setEnable = True
    else:
#        print  date.hour
        if date.hour not in silenthours:
#            print("if internal_temp > target_temp: " +  str(internal_temp) + " " + str(target_temp))
            if internal_temp > target_temp:
                setEnable = True
    if not lastStatus == setEnable:
      lastStatus=setEnable
      if setEnable:
         print("enabled")
         s.send('S PIDS '+modulename+' '+item_name+' -1')
         data = s.recv(1024)
      else:
#         print("internal_temp-1: "+str(internal_temp-1))
         if internal_temp < target_temp-1:
           print("disabled")
           s.send('S PIDS '+modulename+' '+item_name+' 0')
           data = s.recv(1024)
    time.sleep(60)

