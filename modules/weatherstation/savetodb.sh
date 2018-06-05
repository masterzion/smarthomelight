#!/bin/bash

source ~/.bashrc

./savetodb.py $SMARTHOME_MEMDB_PORT $(cat modulename.txt)
