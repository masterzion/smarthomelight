#!/bin/bash
source ~/.bashrc


MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="sound_turnon"


CINEMAMODE_STRING="cinemamode cinemamode_on"
PLAYMUSIC_STRING="music play"
RADIOEMISSOR_STRING="radiotransmitter radio_turnon"


$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULE_NAME $MODULE_ITEM 1 > /dev/null


while true;
do
    RADIOEMISSOR=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G PIDS $RADIOEMISSOR_STRING  )
    if [ "$RADIOEMISSOR" == "" ] ; then 
        RADIOEMISSOR=0
    fi

    if [ "$RADIOEMISSOR" == "0" ] ; then
	    CINEMAMODE=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G PIDS $CINEMAMODE_STRING  )
	    PLAY_MUSIC=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G PIDS $PLAYMUSIC_STRING  )

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
    else
	$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM 0 > /dev/null
    fi

    sleep 20
done

