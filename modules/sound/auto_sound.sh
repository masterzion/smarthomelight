#!/bin/bash
source ~/.bashrc

GPIO=23
gpio -g mode $GPIO out


while true;
do
    HOUR=$(date +"%H")

    # house is empt    
    if [ "$CINEMAMODE" == "1" ] ; then
       gpio -g write $GPIO 0
    else
        # house is empt
        if [ "$HOUSEISEMPT" == "1" ] ; then
            gpio -g write $GPIO 1
        else
            # too late, turn off
            if [ "$HOUR" -ge "$MAX_HOUR" ] ; then
               if [ "$CINEMAMODE" == "0" ] ; then
                   gpio -g write $GPIO 1
               fi
            else
               # not so late, turn on
               gpio -g write $GPIO 0
            fi
        fi
    fi
    sleep 2
done
