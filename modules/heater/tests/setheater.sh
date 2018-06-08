gpio -g mode 24 out

if [ "$1" == "on" ]; then
    gpio -g write 24 0
else
    gpio -g write 24 1
fi
