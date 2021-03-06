#!/bin/bash
#
# require:  mpc
# apt-get install mpc

#!/bin/bash
source ~/.smarthomelight

LASTSTATE="0"

HOUSEISEMPTY_STRING="houseisempty mobile_check"

MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="vickon"

MAX_HOUR=23
MIN_HOUR=10



LAST_STATE="1"
STATE=0

$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM 0  > /dev/null

while true;
do
    # get the actual state
    STATE="0"

    HOUR=$(date +"%H")
    if [ "$HOUR" -ge $MIN_HOUR -a "$HOUR" -le $MAX_HOUR ] ; then
        HOUSEISEMPT=$($SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT G VALUES $HOUSEISEMPTY_STRING)
        if [ "$HOUSEISEMPT" == "0" ]; then
            STATE="-1"
        fi
    fi

    if [ ! "$LAST_STATE" == "$STATE" ] ; then
        $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S PIDS $MODULE_NAME $MODULE_ITEM $STATE > /dev/null
        LAST_STATE=$STATE
    fi

    sleep 120
done
