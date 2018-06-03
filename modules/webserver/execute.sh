#!/bin/bash 
source ~/.bashrc
/usr/bin/python  -m tornado.autoreload   /root/weatherstation/web/webserver.py &> /dev/null