#!/bin/bash

source ~/.bashrc

MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="start_modules"


grep -v  '^#' itens.conf | grep -v -e '^$'  | while read -r line ; do
    echo  "Checking $line... "
    if [ "memorydb memorydb_server" == "$line" ] ; then
       PID="0"
    else
        PID=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G PIDS $line)
    fi

    if [ "$PID" == "" ] ; then
       PID=0
    fi

    if [ "$PID" == "0" ] ; then
       $SMARTHOME_DIR/bin/service_manager.sh start  $line
       sleep 1
    else
       echo "is running."
    fi
done


echo "==========="
echo "Finished!"

$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM -1 > /dev/null

