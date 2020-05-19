#!/bin/bash

source ~/.smarthomelight

./tuya_manager.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)
