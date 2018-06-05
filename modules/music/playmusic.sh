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


MODULE_NAME=$(cat modulename.txt)
MODULE_ITEM="play"


$SMARTHOME_DIR/bin/memdb_client.py 3030 S PIDS $MODULE_NAME $MODULE_ITEM 0 2> /dev/null

MAX_HOUR=22
MIN_HOUR=10

while true;
do
    # get the actual state
    PLAY=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G PIDS $MODULE_NAME $MODULE_ITEM)
    if [ "$PLAY" == "0" ]; then
       SEND_COMMAND="pause"
    else
       SEND_COMMAND="play" #play
    fi
    
    if [ "$SEND_COMMAND" == "play" ]; then
        HOUR=$(date +"%H")
        if [ "$HOUR" -ge $MIN_HOUR -a "$HOUR" -le $MAX_HOUR ] ; then
           mpc -h "$SERVER_NAME" -p "$SERVER_PORT" volume 75 > /dev/null
           mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "$SEND_COMMAND" > /dev/null
        fi
    else
        mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "$SEND_COMMAND" > /dev/null
    fi
    sleep 20
done
