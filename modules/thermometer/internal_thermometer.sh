#!/bin/bash

source ~/.smarthomelight

./internal_thermometer.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)
