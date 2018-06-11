#!/usr/bin/python
import os, sys, socket, time
from subprocess import call

memdb_host = 'localhost'
memdb_port=int(sys.argv[1])


modulename=sys.argv[2]
app_path=sys.argv[3]
modulitem='web_servicemanager'



def sendtext(text):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', memdb_port))
    s.send(text)
    data = s.recv(1024)
#    print text+ ':'+data
    s.close()
    return data.strip()


    

def doaction(start):
    if start:
        action='start'
    else:
        action='stop'

    data=sendtext('G VALUES '+modulename+' '+modulitem+'_'+action)
    
    if data == "":
        data="0"
    
    
    if not data == "0":
        data=data.split(";")
        
        for i in data:
#            print i
            item=i.split('/')
            if len(item) == 2:
#                print [app_path+"/bin/service_manager.sh", action, item[0], item[1] ]
                call([app_path+"/bin/service_manager.sh", action, item[0], item[1] ])
        data=sendtext('S VALUES '+modulename+' '+modulitem+'_'+action+' 0')



sendtext('S VALUES '+modulename+' '+modulitem+'_start 0')
sendtext('S VALUES '+modulename+' '+modulitem+'_stop 0')

# main loop
while True:
    doaction(True)
    doaction(False)
    time.sleep(2)
