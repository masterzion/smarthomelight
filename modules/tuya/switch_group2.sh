#!/bin/bash

source ~/.bashrc

MODULENAME=$(cat modulename.txt)
MODULEITEM='switch_group2'

STATUS=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G VALUES $MODULENAME ${MODULENAME}_manager)

GROUP_STATUS=$(echo $STATUS | awk -F  "," '{print $2}')
if [ "$GROUP_STATUS" -eq "0" ] ; then
   GROUP_STATUS=1
else
   GROUP_STATUS=0
fi

STATUS=$(echo $STATUS | awk -F  "," '{print $1",'$GROUP_STATUS',"$3","$4}')

$SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES $MODULENAME ${MODULENAME}_manager $STATUS
$SMARTHOME_DIR/bin/memdb_client.py 3030 S PID $MODULENAME $MODULEITEM -1