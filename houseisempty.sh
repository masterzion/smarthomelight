#!/bin/bash

. ~/.bashrc

MAX_RETRY=10
SLEEP=10

get_state() {
    IP=$1
    COUNT=$(ping "$IP" -c 5 -W 5 | grep "ttl=" | wc -l)

    if [ $COUNT -eq 0 ]; then
        echo 0
    else
        echo 1
    fi
}


ISEMPT=0
RETRY=1
while true;
do

    for MAC in $MAC_LIST; do
        echo "Cheking $MAC ...."
        IP="$(arp-scan --localnet | grep $MAC  | awk ' { printf $1 } ')"
        ISEMPT=$(get_state $IP)
        if [ $ISEMPT -eq 1 ]; then
           echo "is active "
           break
        else
           echo "is not active "
        fi

    done


    if [ $ISEMPT -eq 0 ]; then
        if [ $RETRY -eq $MAX_RETRY ]; then
           echo "creating file  $FILE_HOUSEISEMPTY ..."
           touch $FILE_HOUSEISEMPTY
        else
            echo "Retry $RETRY"
            RETRY=$((RETRY+1))
        fi
    else
       if [ -f $FILE_HOUSEISEMPTY ]; then
          echo "deleting file  $FILE_HOUSEISEMPTY ..."
          rm -f $FILE_HOUSEISEMPTY
          RETRY=1
       fi
       sleep 90
    fi

    ISEMPT=0
    sleep $SLEEP
done
