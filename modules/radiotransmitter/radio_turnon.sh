#!/bin/bash

source ~/.smarthomelight

MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="radio_turnon"

$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS sound sound_turnon 0 > /dev/null
sleep 4800
$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM 0 > /dev/null
