#!/usr/bin/env python2.7
import os, sys, pytuya, socket, time, ConfigParser

memdb_host = 'localhost'
memdb_port=int(sys.argv[1])
modulename=sys.argv[2]

moduleitem=modulename+'_manager'



configParser = ConfigParser.RawConfigParser()
configFilePath = r'tuya.conf'
configParser.read(configFilePath)

count = int(configParser.get('MAIN', 'COUNT'))

ids = []
ips = []
keys = []
ar_status = []


def getstatus(index):
#    print index
    try:
        d = pytuya.OutletDevice(ids[index], ips[index], keys[index])
        data = d.status()
        return data['dps']['1']
    except:
        print "Unexpected error:", sys.exc_info()[0]
        return False

def setstatus(index, status, count):
    print index,status
    try:
        d = pytuya.OutletDevice(ids[index], ips[index], keys[index])
        data = d.status()  # NOTE this does NOT require a valid key
#        print data
        if not status == data['dps']['1']:
            data = d.set_status(status)
            time.sleep(2)
            data = d.status()
#            print data
            return data
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        time.sleep(2 * count)
        count+=1
        if count < 10:
          return setstatus(index, status, count)
        else:
          return False


def setgroup(status):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((memdb_host, memdb_port))
    text='S VALUES '+modulename+' '+moduleitem+' '+status
#    print text
    s.send(text)
    data = s.recv(1024)
#    print "data:" + data
    if data in ["0", ""]:
        return "0"
    else:
        return "1"



def getgroup(group):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((memdb_host, memdb_port))
    s.send('G PIDS '+modulename+' '+'switch_group'+str(group))
    data = s.recv(1024)
#    print data
    if data == "-1":
        return "1"
    else:
        return "0"

for index in range(count):
#    print index
    ids.append( configParser.get(str(index), 'ID') )
    ips.append( configParser.get(str(index), 'IP') )
    keys.append( configParser.get(str(index), 'KEY') )
    if getstatus(index):
        ar_status.append('1')
    else:
        ar_status.append('0')

#print ar_status
status = ",".join(ar_status)
last_status=status

setgroup(status)

# main loop
while True:
    #get the answer
#    status = getgroup(1)+','+getgroup(2)+','+getgroup(3)+','+getgroup(4)
    status = getgroup(1)+','+getgroup(2)+','+getgroup(3)

#    print status
#    print last_status

    if not status == last_status :
#        for group in [0,1,2,3] :
        for group in [0,1,2] :
            ar_status = status.split(',')
            ar_last_status = last_status.split(',')
#            print ar_last_status[group]
#            print ar_status
            if not ar_last_status[group] == ar_status[group]:
#                print "group "+str(group) + ": "+ ar_status[group]
                migroup=int(group)+1
                if ar_status[group] == '1' :
                    setstatus(group, True, 0)
                else:
                    setstatus(group, False, 0)

    last_status = status
    time.sleep(1)
