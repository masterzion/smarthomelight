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


while true;
do
    # get the actual state
    HOUSEISEMPT=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G VALUES $HOUSEISEMPTY_STRING)

    if [ "$HOUSEISEMPT" == "1" ]; then
        $SMARTHOME_DIR/bin/memdb_client.py 3030 S PIDS $MODULE_NAME $MODULE_ITEM 0 > /dev/null
    else
        CINEMAMODE=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G VALUES $CINEMAMODE_STRING)
        if [ "$CINEMAMODE" == "1" ]; then
            $SMARTHOME_DIR/bin/memdb_client.py 3030 S PIDS $MODULE_NAME $MODULE_ITEM 0 > /dev/null
        else
            $SMARTHOME_DIR/bin/memdb_client.py 3030 S PIDS $MODULE_NAME $MODULE_ITEM -1 > /dev/null
        fi
    fi

    sleep 5
done
