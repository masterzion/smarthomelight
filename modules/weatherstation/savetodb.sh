#!/bin/bash

source ~/.bashrc

/usr/bin/python ./savetodb.py $SMARTHOME_MEMDB_PORT "$(cat modulename.txt)" # >> savetodb.log  2>> error.log
