#!/bin/bash

source ~/.bashrc

./light_sensor.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)
