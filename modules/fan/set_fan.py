#!/usr/bin/python
import os, sys, socket, time

def sendtext(text):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', memdb_port))
    s.send(text)
    data = s.recv(1024)
#    print text+ ':'+data
    s.close()
    return data.strip()

memdb_host = 'localhost'
memdb_port=int(sys.argv[1])
modulename=sys.argv[2]
moduleitem="fan_turnon"
sendtext('S VALUES '+modulename+' '+moduleitem+' 0')

while True:
  value=sendtext('G PIDS '+modulename+' '+moduleitem)
  if value == "":
    value="0"

  if value == "0":
    sendtext('S PIDS tuya switch_group2 0')
  else:
    sendtext('S PIDS tuya switch_group2 -1')
  time.sleep(5)
