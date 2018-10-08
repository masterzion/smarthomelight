#!/bin/bash
source ~/.bashrc

#MAX_RETRY=120
MAX_RETRY=50

AIR_VICK_GPIO=13
MAX_HOUR=23
MIN_HOUR=10

gpio -g mode $AIR_VICK_GPIO out

MODULENAME=$(cat modulename.txt)
ITEMNAME="mobile_check"

$SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES $MODULENAME $ITEMNAME 1 > /dev/null
gpio -g write $AIR_VICK_GPIO 1

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
           gpio -g write $AIR_VICK_GPIO 1
        else
#            echo "Retry $RETRY"
            RETRY=$((RETRY+1))
        fi
    else
        $SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES $MODULENAME $ITEMNAME 0 > /dev/null
        HOUR=$(date +"%H")
        if [ "$HOUR" -ge $MIN_HOUR -a "$HOUR" -le $MAX_HOUR ] ; then
            gpio -g write $AIR_VICK_GPIO 0
        else 
            gpio -g write $AIR_VICK_GPIO 1
        fi
        RETRY=1
        sleep 60
    fi

    ISEMPT=0
done
