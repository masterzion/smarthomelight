#!/usr/bin/env python2.7
import os, sys, socket, time, urllib

memdb_host = 'localhost'
memdb_port=int(sys.argv[1])
modulename=sys.argv[2]
ips=sys.argv[3].split()

#print(ips)
#count(ips)

moduleitem=modulename+'_manager'

count = len(ips)
ar_status = []


def getstatus(index):
#    print index
    try:
        f = urllib.urlopen('http://'+ips[index]+'/?m=1')
        myfile = f.read()
        return myfile.find(">ON<") > -1
    except:
        print "Unexpected error:", sys.exc_info()[0]
        return False

def setstatus(index, status, count):
    count+=1
#    print count,index,status
    try:
        if not getstatus(index) == status:
            f = urllib.urlopen('http://'+ips[index]+'/?m=1&o=1')
            myfile = f.read()
            return myfile.find(">ON<") > -1
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        time.sleep(2 * count)
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
