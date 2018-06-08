#!/bin/bash

source ~/.bashrc

while true;
do
   ./getday.py > $SMARTHOME_DIR/modules/webserver/home/js/day.json
   sleep 120
done