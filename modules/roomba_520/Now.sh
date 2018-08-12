#!/bin/bash

source ~/.bashrc

MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="Now"
sleep 3
$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM 0 > /dev/null

