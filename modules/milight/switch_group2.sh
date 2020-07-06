#!/bin/bash

source ~/.smarthomelight

STATUS=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G VALUES milight light_manager)
MODULENAME=$(cat modulename.txt)

GROUP_STATUS=$(echo $STATUS | awk -F  "," '{print $2}')
if [ "$GROUP_STATUS" -eq "0" ] ; then
   GROUP_STATUS=1
else
   GROUP_STATUS=0
fi

STATUS=$(echo $STATUS | awk -F  "," '{print $1",'$GROUP_STATUS',"$3","$4}')

$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULENAME light_manager $STATUS
