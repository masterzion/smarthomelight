#!/bin/bash
source ~/.bashrc


MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="turn_on"


CINEMAMODE_STRING="cinemamode cinemamode_on"
PLAYMUSIC_STRING="sound play"



$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULE_NAME $MODULE_ITEM 1 > /dev/null


while true;
do
    CINEMAMODE=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G PIDS $CINEMAMODE_STRING  )
    PLAY_MUSIC=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G PIDS $PLAYMUSIC_STRING  )
    ACTIVE="$(($CINEMAMODE + $PLAY_MUSIC))"
    
    # house is empt
    if [ "$ACTIVE" == "0" ] ; then
       $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM 0 > /dev/null
    else
       $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM -1 > /dev/null
    fi

    sleep 5
done
