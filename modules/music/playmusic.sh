#!/bin/bash
# 
# require:  mpc
# apt-get install mpc

#!/bin/bash
source ~/.bashrc

# saver to add in .bashrc ;)
# SERVER_NAME="password@ip" 
echo "Server: $SERVER_NAME"


LASTSTATE="0"


MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="play"


$SMARTHOME_DIR/bin/memdb_client.py 3030 S PIDS $MODULE_NAME $MODULE_ITEM 0 > /dev/null

MAX_HOUR=22
MIN_HOUR=10
MIN_VOL=50

while true;
do
    # get the actual state
    PLAY=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G PIDS $MODULE_NAME $MODULE_ITEM)

    if [ ! "$LASTSTATE" == "$PLAY" ]; then
        if [ "$PLAY" == "0" ]; then
           SEND_COMMAND="pause"
        else
           SEND_COMMAND="play"
        fi

        if [ "$SEND_COMMAND" == "play" ]; then
            HOUR=$(date +"%H")
            if [ "$HOUR" -ge $MIN_HOUR -a "$HOUR" -le $MAX_HOUR ] ; then
               $SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES $MODULE_NAME sound_volume 50 > /dev/null
            else
               $SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES $MODULE_NAME sound_volume 30 > /dev/null
            fi
        fi
        mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "$SEND_COMMAND" > /dev/null
        LASTSTATE=$PLAY
    fi
    if [ "$PLAY" == "0" ]; then
       sleep 3
    fi

    VOLUME=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G VALUES $MODULE_NAME sound_volume)
    VOLUME=`echo "($VOLUME / 2) + $MIN_VOL" | bc`
    VOLUME=${VOLUME%.*}


    mpc -h "$SERVER_NAME" -p "$SERVER_PORT" volume $VOLUME > /dev/null
    sleep 2
done
