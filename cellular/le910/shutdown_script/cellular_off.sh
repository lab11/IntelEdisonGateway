#!/bin/bash

DIRECTORY="/sys/class/gpio/gpio40/"
if [ ! -d "$DIRECTORY" ]; then
    echo 40 > /sys/class/gpio/export
fi
echo "out" > /sys/class/gpio/gpio40/direction
echo 1 > /sys/class/gpio/gpio40/value

stty -F /dev/ttyUSB3 raw -echo -echoe -echok -echoctl -echoke
echo -e -n 'at#shdn\r'  > /dev/ttyUSB3

