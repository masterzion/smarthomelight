#!/bin/bash
# 
# require:  mpc
# apt-get install mpc

#!/bin/bash
source ~/.bashrc
source $SMARTHOME_DIR/bash.lib.sh

echo "Server:"
echo $SERVER_NAME

# saver to add in .bashrc ;)
# MOBILE_IP=""
# SERVER_NAME="password@ip" 

LASTSTATE="-1"

while true;
do
    # get the actual state
    HOUSEISEMPT=$(get_houseisempt)
    CINEMAMODE=$(get_cinemamode)
    HOUR=$(date +"%H")
    
    if [ "$LASTSTATE" == "$HOUSEISEMPT" ]; then
        echo "if found state wasn't changed, wait 3 seconds."
        sleep 2

        if [ "$CINEMAMODE" == "1" ]; then
           SEND_COMMAND="pause"
           mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "$SEND_COMMAND"
        fi
    else
        # if found state was changed
        if [ "$HOUSEISEMPT" == "1" ]; then
           echo "it the state result was not found, pause the music"
           SEND_COMMAND="pause"
        else
           echo "else means the state result was found, play the music"
           SEND_COMMAND="play" #play
        fi

        echo "send command to the server"
	    if [ "$SEND_COMMAND" == "play" ]; then
	        if [ "$HOUR" -ge $MIN_HOUR -a "$HOUR" -le $MAX_HOUR ] ; then
	           echo "but not at $HOUR hs"
	           mpc -h "$SERVER_NAME" -p "$SERVER_PORT" volume 75
	           mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "$SEND_COMMAND"
	        fi
	    else
	        mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "$SEND_COMMAND"
	    fi

        echo "save last state = $HOUSEISEMPT"
        LASTSTATE=$HOUSEISEMPT
    fi
done
