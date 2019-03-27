#!/bin/bash

# wifi up
sudo ifconfig wlan0 up
sleep 1m

# send weight
cd /home/pi/stockwaage
./send_weight.py 1m
./send_weight.py 10m
./send_weight.py 1h
./send_weight.py 1d

# wifi down
sleep 1m
#sudo ifconfig wlan0 down
