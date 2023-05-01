#!/bin/bash

source ~/.smarthomelight

MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="play"
sleep 5
$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM -1 > /dev/null
bluetoothctl connect $(cat bluetooth.txt)
