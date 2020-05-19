#!/bin/bash

source ~/.smarthomelight

MODULENAME=$(cat modulename.txt)

./web_service_manager.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt) $SMARTHOME_DIR > /dev/null

