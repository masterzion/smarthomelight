#!/bin/bash

source ~/.smarthomelight

MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM=cinemamode_on

LAST_STATUS=false

$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES cinemamode auto_cinemamode 0

while true;
do
    CHROMECAST=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G VALUES cinemamode auto_cinemamode)

    if [ "$CHROMECAST" == "0" ]; then
         STATUS=false
    else
         STATUS=true
    fi


    if [ ! "$STATUS" == "$LAST_STATUS" ]; then
      if [ "$STATUS" == "false" ]; then
          $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM 0 > /dev/null
      else
          $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM -1 > /dev/null
      fi
    fi
    LAST_STATUS=STATUS
    sleep 10
done
