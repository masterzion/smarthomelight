#!/bin/bash

.  /root/.bashrc
sleep 20

MILIGHT_IP="$(arp-scan --localnet | grep $MILIGHT_MAC  | awk ' { printf $1 } ')"
/root/weatherstation/startlight.py $FILE_HOUSEISEMPTY $MILIGHT_IP $MILIGHT_PORT $MILIGHT_GROUP
