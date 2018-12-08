#!/bin/bash

source ~/.bashrc

MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM=cinemamode_on

LAST_STATUS=false

while true;
do
    CHROMECAST_IP="$(arp-scan --localnet | grep $CHROMECAST_MAC  | awk ' { printf $1 } ')"
    if [ "$CHROMECAST_IP" == "" ]; then
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
    sleep 40
done
