#!/bin/bash

source ~/.smarthomelight

export MILIGHT_MAC=$(echo "$MILIGHT_MAC" | tr '[:upper:]' '[:lower:]')

MILIGHT_IP="$(sudo /usr/sbin/arp-scan --localnet --interface=$IFACE | grep $MILIGHT_MAC  | awk ' { printf $1 } ')"
#wait for the milight box startup
until [ ! -z "$MILIGHT_IP"  ]; do
  MILIGHT_IP="$(sudo /usr/sbin/arp-scan --localnet --interface=$IFACE | grep $MILIGHT_MAC  | awk ' { printf $1 } ')"
  sleep 10
done



$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULENAME switch_group1_color ff8800
$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULENAME switch_group2_color ff8800
$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULENAME switch_group3_color ff8800
$SMARTHOME_DIR/bin/memdb_client.py $SMARTHOME_MEMDB_PORT S VALUES $MODULENAME switch_group4_color ff8800


./light_manager.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt) $MILIGHT_IP $MILIGHT_PORT
