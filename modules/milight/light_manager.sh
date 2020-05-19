#!/bin/bash

source ~/.smarthomelight

export MILIGHT_MAC=$(echo "$MILIGHT_MAC" | tr '[:upper:]' '[:lower:]')

MILIGHT_IP="$(sudo /usr/sbin/arp-scan --localnet --interface=$IFACE | grep $MILIGHT_MAC  | awk ' { printf $1 } ')"
#wait for the milight box startup
until [ ! -z "$MILIGHT_IP"  ]; do
  MILIGHT_IP="$(sudo /usr/sbin/arp-scan --localnet --interface=$IFACE | grep $MILIGHT_MAC  | awk ' { printf $1 } ')"
  sleep 10
done

./light_manager.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt) $MILIGHT_IP $MILIGHT_PORT
