#!/bin/bash

source ~/.smarthomelight

MODULENAME=$(cat modulename.txt)
FILE_MASK=$(echo $MODULENAME"_" | tr '[a-z]' '[A-Z]')
CRON_PATH=$SMARTHOME_DIR/smartcron/



#Restore status
echo "Restoring the status of $i"

if [ -f $(echo $CRON_PATH$FILE_MASK"Start") ] ; then
   $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULENAME autostart "-1" > /dev/null 
else
   $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULENAME autostart "0" > /dev/null
fi



while true;
do
   STATUS=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G PIDS $MODULENAME autostart )
   FILE=$(echo $CRON_PATH$FILE_MASK"Start")
   if [ "$STATUS" == "0" ] ; then
        if [ -f $FILE ]; then
            rm $CRON_PATH$FILE_MASK*
        fi
   else
        if [ ! -f $FILE ]; then
            cp $SMARTHOME_DIR/modules/$MODULENAME/cron/* $CRON_PATH
        fi
   fi
   sleep 300
done

