#!/bin/bash

source ~/.smarthomelight

MODULENAME=$(cat modulename.txt)

./set_radio.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)

