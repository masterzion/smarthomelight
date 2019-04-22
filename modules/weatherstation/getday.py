#!/usr/bin/python

import json

import threading
import time

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

dataday=""

class MyThread(threading.Thread):
    def run(self):
        global dataday
        from models import Sensors
        while True:
            dataday = json.dumps( Sensors().getDay() )
            time.sleep(30)
        return 

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global dataday
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write( dataday )
        return
    def log_message(self, format, *args):
        return

PORT_NUMBER=8080
server = HTTPServer(('', PORT_NUMBER), myHandler)
th = MyThread()
th.daemon = True
th.start()
try:
    server.serve_forever()
except :
    server.socket.close()
