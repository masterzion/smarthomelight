GPIORADIO=22
GPIOENERNY=5

gpio -g mode $GPIORADIO out
gpio -g mode $GPIOENERNY out


if [ "$1" == "on" ]; then
    gpio -g write $GPIORADIO 0
    gpio -g write $GPIOENERNY 1
else
    gpio -g write $GPIORADIO 1
    gpio -g write $GPIOENERNY 0
fi
