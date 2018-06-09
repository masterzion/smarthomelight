#!/bin/bash

source ~/.bashrc

STATUS=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G VALUES milight light_manager)

GROUP_STATUS=$(echo $STATUS | awk -F  "," '{print $4}')
if [ "$GROUP_STATUS" -eq "0" ] ; then
   GROUP_STATUS=1
else
   GROUP_STATUS=0
fi


STATUS=$(echo $STATUS | awk -F  "," '{print $1","$2","$3",'$GROUP_STATUS'"}')

$SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES milight light_manager $STATUS