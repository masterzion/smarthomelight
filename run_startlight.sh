#!/bin/bash

. /root/.bashrc 
/root/weatherstation/startlight.py $MOBILE_IP $MILIGHT_IP $MILIGHT_PORT $MILIGHT_GROUP
