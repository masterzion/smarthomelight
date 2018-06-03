#!/usr/bin/python
import asyncore, socket, sys

Matrix = {}

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            print "data: "+data+" \n"
            split = data.split(' ')
            operation=split[0]
            if len(split) < 2:
                if conn is not None:
                  self.send("ERROR: Minimum 2 paramters. Check the documentation. ;)\n")
            else:
                if operation == 'L':
                    data=""
                    for values in Matrix.keys():
                        if values[0] == split[1]:
                            data+=values[1]  + ' ' +values[2]+ ' ' + Matrix[values[0], values[1], values[2]] + "\n"
                    self.send( data + "\n" )
                elif operation == 'G':
                    if len(split) < 4:
                      self.send("SERVER ERROR: Get requires 3 paramters.\n")
                    else:
                      self.send( Matrix[ split[1], split[2], split[3] ] )
                elif operation == 'S':
                    if len(split) < 5:
                      self.send("SERVER ERROR: Set requires 4 paramters.\n")
                    else:
                      Matrix[ split[1], split[2], split[3] ] = split[4]
                      self.send("OK\n")


class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock)
            
port= int(sys.argv[1])
if port == "":
   port=3030
   print "Starting in the default port 3030"

server = EchoServer('localhost', port )
asyncore.loop()


