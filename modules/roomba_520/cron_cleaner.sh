#!/bin/bash

source ~/.smarthomelight

MODULENAME=$(cat modulename.txt)

#Restore status
for i in $( ls $SMARTHOME_DIR/modules/roomba_520/cron/ ); do
 echo "Restoring the status of $i"
 if [ -f "$SMARTHOME_DIR/smartcron/ROOMBA_$i" ] ; then
   $SMARTHOME_DIR/bin/memdb_client.py 3030 S PIDS $MODULENAME "${i/ROOMBA_/}" "-1" > /dev/null 
 else
   $SMARTHOME_DIR/bin/memdb_client.py 3030 S PIDS $MODULENAME "${i/ROOMBA_/}" "0" > /dev/null
 fi
done


while true;
do
   for i in $( ls $SMARTHOME_DIR/modules/$MODULENAME/cron/  ); do
       STATUS=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G PIDS $MODULENAME $i 2> /dev/null )
       FILE=$SMARTHOME_DIR/smartcron/ROOMBA_$i
       if [ "$STATUS" == "0" ] ; then
            if [ -f $FILE ]; then
#                echo remove ROOMBA_$i
                rm $FILE
            fi
       else
            if [ ! -f $FILE ]; then
#              echo "copy ROOMBA_$i"
               cp $SMARTHOME_DIR/modules/$MODULENAME/cron/$i $FILE
            fi
       fi
   done
   sleep 50
done


