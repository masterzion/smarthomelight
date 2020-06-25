#!/bin/bash

source ~/.smarthomelight


TUYA_MAC_LIST=$(echo "$TUYA_MAC_LIST" | tr '[:upper:]' '[:lower:]')
TUYA_IP_LIST=""

ACTIVE_IP_MACS="$(sudo /usr/sbin/arp-scan --localnet --interface=$IFACE --quiet --ignoredups  | tail -n +3 | head -n -3 | cut -f2)"
IP=1

for MAC in $TUYA_MAC_LIST; do
  LINE=$(sudo /usr/sbin/arp-scan --localnet --interface=$IFACE --quiet --ignoredups  | tail -n +3 | head -n -3 | grep $MAC)
  IP=$(echo $LINE | cut -f1 -d ' ')

  if [ "$IP" ==  "" ]; then
    IP="192.0.2.1"
  fi

  TUYA_IP_LIST="$TUYA_IP_LIST $IP"
done


./tuya_manager.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt) "$TUYA_IP_LIST"
