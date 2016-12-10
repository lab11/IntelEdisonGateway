#!/bin/bash

if [ -z ${1+x} ]; then 
    echo "binary is missing, useage: ./flash2538.sh fileName.bin"; 
else 
    DIRECTORY="/sys/class/gpio/gpio45/"
    if [ ! -d "$DIRECTORY" ]; then
        echo 45 > /sys/class/gpio/export
    fi
    echo "out" > /sys/class/gpio/gpio45/direction
    echo 1 > /sys/class/gpio/gpio45/value
    python cc2538-bsl.py -b 115200 -e -w -v  $1
    echo 0 > /sys/class/gpio/gpio45/value
fi

