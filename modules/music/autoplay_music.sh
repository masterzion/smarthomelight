#!/bin/bash
# 
# require:  mpc
# apt-get install mpc

#!/bin/bash
source ~/.bashrc

# saver to add in .bashrc ;)
# SERVER_NAME="password@ip" 
echo "Server: $SERVER_NAME"


LASTSTATE="-1"


HOUSEISEMPTY_STRING="houseisempty mobile_check"
CINEMAMODE_STRING="cinemamode cinemamode_on"

MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="autoplay_music"


while true;
do
    # get the actual state
    HOUSEISEMPT=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G VALUES $HOUSEISEMPTY_STRING)

   
    if [ "$LASTSTATE" == "$HOUSEISEMPT" ]; then
        sleep 2

        CINEMAMODE=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G VALUES $CINEMAMODE_STRING)
        if [ "$CINEMAMODE" == "1" ]; then
            $SMARTHOME_DIR/bin/memdb_client.py 3030 S PIDS $MODULE_NAME $MODULE_ITEM -1
        fi
    else
        # if found state was changed
        if [ "$HOUSEISEMPT" == "1" ]; then
            $SMARTHOME_DIR/bin/memdb_client.py 3030 S PIDS $MODULE_NAME $MODULE_ITEM 0
        else
            $SMARTHOME_DIR/bin/memdb_client.py 3030 S PIDS $MODULE_NAME $MODULE_ITEM -1
        fi

        LASTSTATE=$HOUSEISEMPT
    fi
done
