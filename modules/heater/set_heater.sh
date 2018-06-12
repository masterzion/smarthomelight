#!/bin/bash

source ~/.bashrc

MODULENAME=$(cat modulename.txt)

./set_heater.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)

