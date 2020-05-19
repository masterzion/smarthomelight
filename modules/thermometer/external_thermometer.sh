#!/bin/bash

source ~/.smarthomelight

./external_thermometer.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)
