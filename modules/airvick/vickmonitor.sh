#!/bin/bash
source ~/.smarthomelight

MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="vickon"

AIR_VICK_GPIO=13

$GPIO -g mode $AIR_VICK_GPIO  out
$GPIO -g write $AIR_VICK_GPIO 1

$SMARTHOME_DIR/bin/memdb_client.py 3030 S PIDS $MODULE_NAME $MODULE_ITEM 0 > /dev/null

while true;
do
    # get the actual state
    VICK=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G PIDS $MODULE_NAME $MODULE_ITEM)

    if [ "$VICK" == "0" ]; then
       $GPIO -g write $AIR_VICK_GPIO 1
       $SMARTHOME_DIR/bin/service_manager.sh stop tuya switch_group1 > /dev/null
    else
       $GPIO -g write $AIR_VICK_GPIO 0
       $SMARTHOME_DIR/bin/service_manager.sh start tuya switch_group1 > /dev/null
    fi
    sleep 10
done
