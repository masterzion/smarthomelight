
GPIOID=26
gpio -g mode $GPIOID  out

if [ "$1" == "on" ]; then
    gpio -g write  $GPIOID 1
else
    gpio -g write  $GPIOID 0
fi
