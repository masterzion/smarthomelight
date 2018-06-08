#!/bin/bash

source ~/.bashrc

MILIGHT_GROUP=1

#wait for the milight box startup
until [ ! -z "$MILIGHT_IP"  ]; do
  MILIGHT_IP="$(arp-scan --localnet | grep $MILIGHT_MAC  | awk ' { printf $1 } ')"
  sleep 1
done


./auto_light_sensor.py $SMARTHOME_MEMDB_PORT $MILIGHT_IP $MILIGHT_PORT $MILIGHT_GROUP
