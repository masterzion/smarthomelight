#!/bin/bash 

source ~/.bashrc

cd "$SMARTHOME_DIR/modules/webserver/home"
authbind --deep /usr/bin/python  -m tornado.autoreload webserver.py $SMARTHOME_MEMDB_PORT 80

