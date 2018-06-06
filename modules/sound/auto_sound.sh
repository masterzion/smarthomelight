#!/bin/bash
source ~/.bashrc


MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="turn_on"


CINEMAMODE_STRING="cinemamode cinemamode_on"
PLAYMUSIC_STRING="music play"



$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULE_NAME $MODULE_ITEM 1 > /dev/null


while true;
do
    CINEMAMODE=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G PIDS $CINEMAMODE_STRING  )
    PLAY_MUSIC=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G PIDS $PLAYMUSIC_STRING  )

    if [ "$CINEMAMODE" == "" ] ; then
        CINEMAMODE=0
    fi


    if [ "$PLAY_MUSIC" == "" ] ; then 
        PLAY_MUSIC=0
    fi

    ACTIVE="$CINEMAMODE$PLAY_MUSIC"

    # house is empt
    if [ "$ACTIVE" == "00" ] ; then
       $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM 0 > /dev/null
    else
       $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM -1 > /dev/null
    fi

    sleep 10
done
