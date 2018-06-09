#!/bin/bash
source ~/.bashrc

#MAX_RETRY=120
MAX_RETRY=50
SLEEP=20

MODULENAME=$(cat modulename.txt)
ITEMNAME="mobile_check"

$SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES $MODULENAME $ITEMNAME 1 > /dev/null

get_state() {
    IP=$1
    COUNT=$(ping "$IP" -c 5 -W 5 | grep "ttl=" | wc -l)

    if [ $COUNT -eq 0 ]; then
        echo 0
    else
        echo 1
    fi
}


ISEMPT=1
RETRY=1
while true;
do
    for MAC in $MAC_LIST; do
        IP="$(arp-scan --localnet | grep $MAC  | awk ' { printf $1 } ')"
#        echo "Cheking $MAC - IP $IP - TRY - $RETRY / $MAX_RETRY"
        if [ ! -z "$IP" ]; then
            ISEMPT=1
#           echo "is active "
           break
        else
           ISEMPT=0
#           echo "is not active "
        fi
    done


    if [ $ISEMPT -eq 0 ]; then
        sleep 5
        if [ $RETRY -eq $MAX_RETRY ]; then
           $SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES $MODULENAME $ITEMNAME 1 > /dev/null
        else
#            echo "Retry $RETRY"
            RETRY=$((RETRY+1))
        fi
    else
        sleep $SLEEP
        $SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES $MODULENAME $ITEMNAME 0 > /dev/null
        RETRY=1
    fi
    ISEMPT=0
done
