#!/bin/bash

source ~/.smarthomelight

while :
do
  ./external_thermometer.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)
  sleep 1
done

