#!/bin/bash

source ~/.bashrc

MODULE_NAME=$(cat modulename.txt)
./auto_fan.py $SMARTHOME_MEMDB_PORT $MODULE_NAME 