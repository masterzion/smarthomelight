#!/bin/bash

source ~/.smarthomelight
MODULENAME=$(cat modulename.txt)
ITEMNAME="getday"

while true;
do
   ./getday.py > $SMARTHOME_DIR/modules/webserver/home/js/day.json
   sleep 120
done

