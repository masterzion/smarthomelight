#!/bin/bash
# 
# require:  mpc
# apt-get install mpc

source ~/.bashrc

MIN_HOUR=11
MAX_HOUR=22



# saver to add in .bashrc ;)
# MOBILE_IP=""
# SERVER_NAME="password@ip" 

echo "Server:"
echo $SERVER_NAME

function get_state() {
  if [ -f $FILE_HOUSEISEMPTY ]; then
     echo 0
   else
     echo 1
   fi

}

LASTSTATE="-1"

while true;
do
    # get the actual state
    STATE=$(get_state)

    if [ "$LASTSTATE" == "$STATE" ]; then
        echo "if found state wasn't changed, wait 3 seconds."
        sleep 2
    else
        # if found state was changed
        if [ "$STATE" == "0" ]; then
           echo "it the state result was not found, pause the music"
           SEND_COMMAND="pause"
        else
           echo "else means the state result was found, play the music"
           SEND_COMMAND="play" #play
        fi

        echo "send command to the server"
	if [ "$SEND_COMMAND" == "play" ]; then
	    HOUR=$(date +"%H")
	    if [ "$HOUR" -ge $MIN_HOUR -a "$HOUR" -le $MAX_HOUR ] ; then
	       echo "but not at $HOUR hs"
	       mpc -h "$SERVER_NAME" -p "$SERVER_PORT" volume 75
	       mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "$SEND_COMMAND"
	    fi
	else
	    mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "$SEND_COMMAND"
	fi

        echo "save last state = $STATE"
        LASTSTATE=$STATE
    fi
done
