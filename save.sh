#!/bin/bash

# params
metric=$1
if [ -z "$metric" ];
then
    echo "Metric angeben: 1m, 10m, 1h oder 1d"
    echo "use e.g. ./save.sh 1m"
    exit 1
fi

metric_array[0]="1m"
metric_array[1]="10m"
metric_array[2]="1h"
metric_array[3]="1d"
if [[ ! " ${metric_array[*]} " == *" ${metric} "* ]];
then
    echo "Metric muss sein: 1m, 10m, 1h oder 1d"
    exit 1
fi

# send data
cd /home/pi/stockwaage
CRON=$(awk -F "=" '/CRON/ {print $2}' config.ini)
if [ ! -z "$CRON" ] && [ $CRON = "ON" ];
then
    ./save.py $metric
fi
