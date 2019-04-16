#!/bin/bash

source ~/.bashrc

MAX_RETRY=100

MODULENAME=$(cat modulename.txt)
ITEMNAME="mobile_check"

$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULENAME $ITEMNAME 1 > /dev/null

ISEMPT=1
RETRY=1
#echo $MAC_LIST
while true;
do
    ACTIVE_MACS="$(arp-scan --localnet --interface=wlan1 --quiet --ignoredups  | tail -n +3 | head -n -3 | cut -f2)"
    CHROMECAST="0"
    ISEMPT="1"
    for ACTIVEMAC in $ACTIVE_MACS; do
#        echo $ACTIVEMAC

        if [ "$ACTIVEMAC" ==  "$CHROMECAST_MAC" ]; then
#          echo "C"
          CHROMECAST="1"
        fi

        for MAC in $MAC_LIST; do
#           echo "M"
           if [ "$MAC" ==  "$ACTIVEMAC" ]; then
             ISEMPT="0"
             break
           fi
       done

    done

#    echo "CHROMECAST  $CHROMECAST"
#    echo "ISEMPT $ISEMPT"

    if [ "$CHROMECAST" == "1" ]; then
#        echo "Chromecast online = 3"
        $SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES cinemamode auto_cinemamode 3 > /dev/null
        sleep 60
    else
        VAL=$($SMARTHOME_DIR/bin/memdb_client.py 3030 G VALUES cinemamode auto_cinemamode)
        if [ $VAL -gt 0 ]; then
           VAL=$((VAL-1))
        fi
#        echo "Chromecast offline  $VAL"
        $SMARTHOME_DIR/bin/memdb_client.py 3030 S VALUES cinemamode auto_cinemamode $VAL > /dev/null
    fi

    if [ $ISEMPT == "1" ]; then
        sleep 20
#        echo " $RETRY -eq $MAX_RETRY"
        if [ $RETRY -eq $MAX_RETRY ]; then
           $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULENAME $ITEMNAME 1 > /dev/null
        else
#            echo "Retry $RETRY"
            RETRY=$((RETRY+1))
        fi
    else
#        echo "not empty"
        $SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULENAME $ITEMNAME 0 > /dev/null
        sleep 50
        RETRY=1
    fi
done
