#!/bin/bash

source ~/.bashrc

MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="cinemamode_on"
sleep 3
echo "cleaning"
$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM -1 > /dev/null

