#!/bin/bash

source ~/.smarthomelight

./internal_light_sensor.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)
