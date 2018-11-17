#!/bin/bash
source ~/.bashrc
./memorydb.py $SMARTHOME_MEMDB_PORT &> /dev/null
sleep 50
