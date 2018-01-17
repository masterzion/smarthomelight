#!/bin/bash

.  /root/.bashrc 
/root/weatherstation/startlight.py $FILE_HOUSEISEMPTY $MILIGHT_IP $MILIGHT_PORT $MILIGHT_GROUP
