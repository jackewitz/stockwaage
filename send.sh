#!/bin/bash

# wifi up
WLAN=$(iwgetid)
if [[ ! "$WLAN" = *wlan* ]]; then
   sudo ifconfig wlan0 up
   sleep 1m
fi

# send data
cd /home/pi/stockwaage
./send.py 1m
./send.py 10m
./send.py 1h
./send.py 1d

# wifi down
TURNWLAN=$(awk -F "=" '/WLAN/ {print $2}' config.ini)
if [ $TURNWLAN = "OFF" ]; then
   sleep 1m
   #sudo ifconfig wlan0 down
fi
