import asyncore
import socket

Matrix = {}

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            print "data: "+data+" \n"
            split = data.split(' ')
            if len(split) < 2:
                if conn is not None:
                  self.send("ERROR: Minimum 2 paramters. Check the documentation. ;)\n")
            else:
                if split[0] == 'L':
                    data=""
                    for values in Matrix.keys():
                        if values[0] == split[1]:
                            data+=values[1]  + ' ' + Matrix[values[0], values[1]] + "\n"
                    self.send( data + "\n" )
                elif split[0] == 'G':
                    if len(split) < 3:
                      self.send("ERROR: Minimum 3 paramters for get operation. Check the documentation. ;)\n")
                    else:
                      self.send( Matrix[ split[1], split[2] ] )
                elif split[0] == 'S':
                    if len(split) < 4:
                      conn.send("ERROR: Minimum 4 paramters for set operation. Check the documentation. ;)\n")
                    else:
                      Matrix[ split[1], split[2] ] = split[3]
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

server = EchoServer('localhost', 3030)
asyncore.loop()


