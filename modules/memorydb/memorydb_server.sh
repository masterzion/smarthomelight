#!/bin/bash
source ~/.smarthomelight
./memorydb.py $SMARTHOME_MEMDB_PORT  &> /dev/null
sleep 50
