#!/bin/bash

source ~/.smarthomelight

MODULENAME=$(cat modulename.txt)
MODULE_ITEM="switch_group1_color"

SWITCH_NAME="switch_group1"

STATUS=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G VALUES milight switch_group1)
DEFAULT_COLOR="ff8800"

if [ "$STATUS" ==  "" ] ; then
  STATUS="ffffff"
fi

if [ "$STATUS" == "$DEFAULT_COLOR" ] ; then
   COLOR="ffffff"
else
   COLOR=$DEFAULT_COLOR
fi

$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULENAME $SWITCH_NAME $COLOR
sleep 10
$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULENAME $MODULE_ITEM 0

