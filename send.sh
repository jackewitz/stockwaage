#!/bin/bash

# wifi up
sudo ifconfig wlan0 up
sleep 1m

# send data
cd /home/pi/stockwaage
./send.py 1m
./send.py 10m
./send.py 1h
./send.py 1d

# wifi down
sleep 1m
#sudo ifconfig wlan0 down
