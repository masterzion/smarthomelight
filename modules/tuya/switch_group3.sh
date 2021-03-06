#!/bin/bash

source ~/.smarthomelight

MODULENAME=$(cat modulename.txt)
MODULEITEM='switch_group3'

STATUS=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G VALUES $MODULENAME ${MODULENAME}_manager)

GROUP_STATUS=$(echo $STATUS | awk -F  "," '{print $3}')
if [ "$GROUP_STATUS" -eq "0" ] ; then
   GROUP_STATUS=1
else
   GROUP_STATUS=0
fi


STATUS=$(echo $STATUS | awk -F  "," '{print $1","$2",'$GROUP_STATUS',"$4}')

$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULENAME ${MODULENAME}_manager $STATUS
sleep 5
$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULENAME $MODULEITEM -1
