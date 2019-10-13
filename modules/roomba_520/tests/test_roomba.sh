#!/bin/bash

while true; do
    echo "Sending..."
    /usr/bin/irsend SEND_ONCE  iRobot_Roomba clean --count 5
    sleep 1
done
