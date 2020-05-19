#!/bin/bash

source ~/.smarthomelight

MODULENAME=$(cat modulename.txt)

./set_fan.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)

