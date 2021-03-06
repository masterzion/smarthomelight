#!/bin/bash

source ~/.smarthomelight
while :
do
  /usr/bin/python ./savetodb.py $SMARTHOME_MEMDB_PORT "$(cat modulename.txt)" # >> savetodb.log  2>> error.log
  sleep 1
  echo "crash.. running again.."
done
