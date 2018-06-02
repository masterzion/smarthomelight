#!/bin/bash

. ~/.bashrc

MAX_RETRY=100
SLEEP=20

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
        IP="$(arp-scan --localnet | grep $MAC  | awk ' { printf $1 } ')"
        echo "Cheking $MAC - IP $IP - TRY - $RETRY / $MAX_RETRY"

#        ISEMPT=$(get_state $IP)
#        if [ $ISEMPT -eq 1 ]; then
        if [ ! -z "$IP" ]; then
            ISEMPT=1
#           echo "is active "
           break
        else
           ISEMPT=0
           sleep $SLEEP
#           echo "is not active "
        fi

    done


    if [ $ISEMPT -eq 0 ]; then
        if [ $RETRY -eq $MAX_RETRY ]; then
           date
           echo "creating file  $FILE_HOUSEISEMPTY ..."
           touch $FILE_HOUSEISEMPTY
        else
#            echo "Retry $RETRY"
            RETRY=$((RETRY+1))
        fi
    else
       if [ -f $FILE_HOUSEISEMPTY ]; then
          date
          echo "deleting file  $FILE_HOUSEISEMPTY ..."
          rm -f $FILE_HOUSEISEMPTY
          RETRY=1
       fi
    fi
    sleep 5
    ISEMPT=0
done
