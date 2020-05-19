#!/bin/bash

source ~/.smarthomelight

./auto_light_sensor.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)
