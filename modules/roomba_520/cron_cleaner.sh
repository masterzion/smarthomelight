#!/bin/bash

source ~/.bashrc


#Restore status
for i in $( ls $SMARTHOME_DIR/modules/roomba_520/cron/ ); do
 echo "Restoring the status of $i"
 if [ -f "/etc/cron.d/ROOMBA_$i" ] ; then
   $SMARTHOME_DIR/bin/memdb_client.py 3030 S PIDS roomba_520 "${i/ROOMBA_/}" "-1" > /dev/null 
 else
   $SMARTHOME_DIR/bin/memdb_client.py 3030 S PIDS roomba_520 "${i/ROOMBA_/}" "0" > /dev/null
 fi
done


while true;
do
   for i in $( ls $SMARTHOME_DIR/modules/roomba_520/cron/  ); do
       STATUS=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G PIDS roomba_520 $i 2> /dev/null )
       FILE=/etc/cron.d/ROOMBA_$i
       if [ "$STATUS" == "0" ] ; then
            if [ -f $FILE ]; then
#                echo remove ROOMBA_$i
                rm $FILE
            fi
       else
            if [ ! -f $FILE ]; then
#              echo "copy ROOMBA_$i"
               cp $SMARTHOME_DIR/modules/roomba_520/cron/$i $FILE
            fi
       fi
   done
   sleep 45
done


