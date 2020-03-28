#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/KVBMonitor
sleep 60
source bin/activate
sudo bin/python kvb-monitor.py --led-rows=32 --led-cols=64 --led-brightness=30 --led-pwm-lsb-nanoseconds=50
cd /
