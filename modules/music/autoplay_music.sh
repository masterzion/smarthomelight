#!/bin/bash
# 
# require:  mpc
# apt-get install mpc

#!/bin/bash
source ~/.bashrc

LASTSTATE="0"

HOUSEISEMPTY_STRING="houseisempty mobile_check"
CINEMAMODE_STRING="cinemamode cinemamode_on"

MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="play"

MAX_HOUR=21
MIN_HOUR=10
LAST_STATE="0"
STATE=0


while true;
do
    # get the actual state
    HOUSEISEMPT=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G VALUES $HOUSEISEMPTY_STRING)

    if [ "$HOUSEISEMPT" == "1" ]; then
        STATE=0
    else
        CINEMAMODE=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G VALUES $CINEMAMODE_STRING)
        if [ "$CINEMAMODE" == "1" ]; then
            STATE=0
        else
            HOUR=$(date +"%H")
            if [ "$HOUR" -ge $MIN_HOUR -a "$HOUR" -le $MAX_HOUR ] ; then
                STATE="-1"
            fi
        fi
    fi

    if [ ! "$LAST_STATE" == "$STATE" ] ; then
        $SMARTHOME_DIR/bin/memdb_client.py 3030 S PIDS $MODULE_NAME $MODULE_ITEM $STATE > /dev/null
        LAST_STATE=$STATE
    fi

    sleep 30
done
