#!/bin/bash

source ~/.bashrc

MILIGHT_MAC=$(cat milight_port.conf | grep 'MAC'  | awk '{print $2}')
MILIGHT_PORT=$(cat milight_port.conf | grep 'PORT'  | awk '{print $2}')

#wait for the milight box startup
until [ ! -z "$MILIGHT_IP"  ]; do
  MILIGHT_IP="$(arp-scan --localnet | grep $MILIGHT_MAC  | awk ' { printf $1 } ')"
  sleep 5
done

./light_manager.py $MILIGHT_IP $MILIGHT_PORT
