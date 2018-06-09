#!/bin/bash
source ~/.bashrc

MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="heater_on"

GPIO=26

VALUE=1
gpio -g mode $GPIO out
gpio -g write $GPIO 0


$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM $VALUE 2> /dev/null

while true;
do
    VALUE=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G PIDS $MODULE_NAME $MODULE_ITEM) # 2> /dev/null

    if [ "$VALUE" == "0" ] ; then
       gpio -g write $GPIO 1
    else
       gpio -g write $GPIO 0
    fi
    sleep 60
done