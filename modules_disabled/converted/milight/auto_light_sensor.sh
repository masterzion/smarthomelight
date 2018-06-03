#!/bin/bash

.  /root/.bashrc

#wait for the milight box startup
until [ ! -z "$MILIGHT_IP"  ]; do
  MILIGHT_IP="$(arp-scan --localnet | grep $MILIGHT_MAC  | awk ' { printf $1 } ')"
  sleep 5
done


/root/weatherstation/auto_light.py $FILE_HOUSEISEMPTY $MILIGHT_IP $MILIGHT_PORT $MILIGHT_GROUP
