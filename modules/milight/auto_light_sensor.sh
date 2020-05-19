#!/bin/bash

source ~/.smarthomelight

MILIGHT_GROUP=1

./auto_light_sensor.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)
