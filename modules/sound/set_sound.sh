#!/bin/bash

source ~/.smarthomelight

MODULENAME=$(cat modulename.txt)
./set_sound.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)

