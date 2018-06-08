#!/bin/bash

source ~/.bashrc

./internal_thermometer.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)
