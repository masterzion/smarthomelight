#!/usr/bin/python
# Echo client program
import socket,sys

split = sys.argv

if len(split) < 4:
    if len(split) == 1:
        cmd = split[0];
        print "Usage:\n"
        print "  SET: "+cmd+" S TABLE ITEM VALUE"
        print "  GET: "+cmd+" G TABLE ITEM"
        print " LIST: "+cmd+" L TABLE\n"
        print "Example:\n"
        print " "+cmd+" S values thermometer 25.9"
        print " "+cmd+" G pids thermometer"
        print " "+cmd+" L values\n"
    else:
        print "ERROR: Minimum 3 paramters. Check the documentation. ;)\n"
else:
    HOST = 'localhost'
    PORT = int(split[1])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    operation=split[2]
    table=split[3]
    # list table
    if operation == 'L':
      s.send(operation+' '+table)
      data = s.recv(1024)
    # get item value
    elif operation == 'G':
        if len(split) < 3:
          print("ERROR: Minimum 3 paramters for get operation. Check the documentation. ;)\n")
        else:
          item=split[4]
          s.send(operation+' '+table+' '+item)
          data = s.recv(1024)
    elif operation == 'S':
        if len(split) < 4:
          print("ERROR: Minimum 4 paramters for set operation. Check the documentation. ;)\n")
        else:
          item=split[4]
          value=split[5] 
          s.send(operation+' '+table+' '+item+' '+value)
          data = s.recv(1024)
    print data.strip()
    s.close()

