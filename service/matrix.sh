#!/bin/bash

brightness=40
columns=32
rows=64

if [ ! $(id -u) -eq 0 ]; then
    echo "Muss als root ausgeführt werden"
    exit 1
fi

sudo bin/python kvb-test.py --led-cols=$columns -r$rows -b$brightness