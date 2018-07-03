#!/bin/bash

source ~/.bashrc

./tuya_manager.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)
