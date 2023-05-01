#!/bin/bash
#
# require:  mpc
# apt-get install mpc

#!/bin/bash
source ~/.smarthomelight

# saver to add in .bashrc ;)
# SERVER_NAME="password@ip"
LASTSTATE="-2"

DEFAULT_PLAYLIST=$(cat defaultplaylist.txt)
RADIO_PLAYLIST=$(cat radioplaylist.txt)

MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="play"

mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "pause" > /dev/null

RADIOEMISSOR_STRING="radiotransmitter radio_turnon"

LAST_VOLUME=0
MAX_HOUR=22
MIN_HOUR=30
MIN_VOL=40
LASTPLAYLIST=""

addplaylists () {
    if [ ! "$LASTPLAYLIST" == "$1" ]; then
       mpc -h "$SERVER_NAME" -p "$SERVER_PORT"  clear > /dev/null
       LASTPLAYLIST="$1"
       for l in $1 ; do
          mpc -h "$SERVER_NAME" -p "$SERVER_PORT"  load $l > /dev/null
       done
       mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "random" "on" > /dev/null
       mpc -h "$SERVER_NAME" -p "$SERVER_PORT"  play > /dev/null
       mpc -h "$SERVER_NAME" -p "$SERVER_PORT"  next > /dev/null
       bluetoothctl connect $(cat bluetooth.txt)
   fi
}

while true;
do
    # get the actual state
    PLAY=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G PIDS $MODULE_NAME $MODULE_ITEM)
    PLAY=1

    if [ ! "$LASTSTATE" == "$PLAY" ]; then
        if [ "$PLAY" == "0" ]; then
           SEND_COMMAND="pause"
        else
           SEND_COMMAND="play"
        fi

        if [ "$SEND_COMMAND" == "play" ]; then
            HOUR=$(date +"%H")
            if [ "$HOUR" -ge $MIN_HOUR -a "$HOUR" -le $MAX_HOUR ] ; then
               $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULE_NAME sound_volume 40 > /dev/null
            else
               $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULE_NAME sound_volume 20 > /dev/null
            fi

         else
            mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "$SEND_COMMAND" > /dev/null
        fi

        LASTSTATE=$PLAY
        sleep 10

        mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "$SEND_COMMAND" > /dev/null
    fi
    if [ "$PLAY" == "0" ]; then
       sleep 3
    fi


    RADIOEMISSOR=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G PIDS $RADIOEMISSOR_STRING  )
    if [ "$RADIOEMISSOR" == "" ] ; then
        RADIOEMISSOR=0
    fi

    if [ "$RADIOEMISSOR" == "0" ] ; then
        VOLUME=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G VALUES $MODULE_NAME sound_volume)
        VOLUME=`echo "($VOLUME / 2) + $MIN_VOL" | bc`
        VOLUME=${VOLUME%.*}
        if [ ! "$LAST_VOLUME" == "$VOLUME" ] ; then
          mpc -h "$SERVER_NAME" -p "$SERVER_PORT" volume $VOLUME > /dev/null
          LAST_VOLUME=$VOLUME
        fi
        addplaylists $DEFAULT_PLAYLIST
    else
        sleep 6
        VOLUME=100
        if [ ! "$LAST_VOLUME" == "$VOLUME" ] ; then
           mpc -h "$SERVER_NAME" -p "$SERVER_PORT" volume $VOLUME > /dev/null
           LAST_VOLUME=$VOLUME
        fi
        addplaylists $RADIO_PLAYLIST
    fi

    sleep 2
done
