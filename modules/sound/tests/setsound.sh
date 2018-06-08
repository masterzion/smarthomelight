gpio -g mode 23 out

if [ "$1" == "on" ]; then
    gpio -g write 23 0
else
    gpio -g write 23 1
fi
