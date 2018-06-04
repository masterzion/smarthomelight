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

# TODO
CINEMAMODE="0"

MAX_HOUR=22
MIN_HOUR=10

while true;
do
    # get the actual state
    HOUSEISEMPT=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G VALUES houseisempty mobile_check)

    HOUR=$(date +"%H")
    
    if [ "$LASTSTATE" == "$HOUSEISEMPT" ]; then
#        echo "if found state wasn't changed, wait 3 seconds."
        sleep 2

        if [ "$CINEMAMODE" == "1" ]; then
           SEND_COMMAND="pause"
           mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "$SEND_COMMAND" 2> /dev/null
        fi
    else
        # if found state was changed
        if [ "$HOUSEISEMPT" == "1" ]; then
#           echo "it the state result was not found, pause the music"
           SEND_COMMAND="pause"
        else
#           echo "else means the state result was found, play the music"
           SEND_COMMAND="play" #play
        fi

#        echo "send command to the server"
	    if [ "$SEND_COMMAND" == "play" ]; then
	        if [ "$HOUR" -ge $MIN_HOUR -a "$HOUR" -le $MAX_HOUR ] ; then
	           $SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES sound set_sound 1
#	           echo "but not at $HOUR hs"
	           mpc -h "$SERVER_NAME" -p "$SERVER_PORT" volume 75 > /dev/null
	           mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "$SEND_COMMAND" > /dev/null
	        fi
	    else
	        mpc -h "$SERVER_NAME" -p "$SERVER_PORT" "$SEND_COMMAND" > /dev/null
	    fi

 #       echo "save last state = $HOUSEISEMPT"
        LASTSTATE=$HOUSEISEMPT
    fi
done
