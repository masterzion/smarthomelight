#!/bin/bash

source ~/.bashrc

./external_thermometer.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)
