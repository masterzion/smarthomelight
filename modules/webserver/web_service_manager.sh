#!/bin/bash

source ~/.bashrc

MODULENAME=$(cat modulename.txt)
ITEMNAME="web_servicemanager"
$SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES $MODULENAME $ITEMNAME"_start" "0" > /dev/null
$SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES $MODULENAME $ITEMNAME"_stop" "0" > /dev/null

while true;
do
    DATA=$( $SMARTHOME_DIR/bin/memdb_client.py 3030 G VALUES $MODULENAME $ITEMNAME"_start")
    if [ ! $DATA == "0" ] ; then
        DATA=$(echo $DATA |  tr ";" " ")
#        echo $DATA
        for I in $DATA ; do
           ITEM=$(echo $I |  tr "/" " ")
           $SMARTHOME_DIR/bin/service_manager.sh start $ITEM > /dev/null
        done
        $SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES $MODULENAME $ITEMNAME"_start" "0" > /dev/null
    fi

    DATA=$( $SMARTHOME_DIR/bin/memdb_client.py 3030 G VALUES $MODULENAME $ITEMNAME"_stop")
    if [ ! $DATA == "0" ] ; then
        DATA=$(echo $DATA |  tr ";" " ")
#        echo $DATA
        for I in $DATA ; do
           ITEM=$(echo $I |  tr "/" " ")
           $SMARTHOME_DIR/bin/service_manager.sh stop $ITEM > /dev/null
        done
        $SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES $MODULENAME $ITEMNAME"_stop" "0" > /dev/null
    fi
    sleep 2
done


