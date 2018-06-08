#!/usr/bin/python
# Echo client program
import socket,sys

split = sys.argv

if len(split) < 3:
    if len(split) == 1:
        cmd = split[0];
        print "Usage:\n"
        print "  SET: "+cmd+" PORT S TABLE MODULE ITEM VALUE"
        print "  GET: "+cmd+" PORT G TABLE MODULE ITEM"
        print " LIST: "+cmd+" PORT L TABLE\n"
        print "Example:\n"
        print " "+cmd+" 3030 S VALUES thermometer internal 25.9"
        print " "+cmd+" 3030 G VALUES thermometer internal"
        print " "+cmd+" 3030 L PIDS\n"
    else:
        print "ERROR: Minimum 4 paramters. Check the documentation. ;)\n"
else:
    #connect to the server
    host = 'localhost'
    port= int(sys.argv[1])
    if port == "":
       port=3030
       print "Connecting in the default port 3030"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    
    operation=split[2]
    table=split[3]
    # list table
    data=""
    if operation == 'L':
        s.send(operation+' '+table)
        data = s.recv(1024)
    # get item value
    else:
        if operation == 'G':
            if len(split) < 6:
                print("CLIENT ERROR: Get requires 4 paramters. Check the documentation. ;)\n")
                sys.exit(2)
            else:
                module=split[4]
                item=split[5]
                s.send(operation+' '+table+' '+module+' '+item)
                data = s.recv(1024)
        elif operation == 'S':
            if len(split) < 7:
                print("CLIENT ERROR: Get requires 6 paramters. Check the documentation. ;)\n")
                sys.exit(2)
            else:
                module=split[4]
                item=split[5]

                value=split[6]
                s.send(operation+' '+table+' '+module+' '+item+' '+value)

                data = s.recv(1024)
    print data.strip()
    s.close()

