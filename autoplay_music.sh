#!/bin/bash
# 
# require:  mpc
# apt-get install mpc

source ~/.bashrc

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
        mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "$SEND_COMMAND"

        echo "save last state = $STATE"
        LASTSTATE=$STATE
    fi
done
