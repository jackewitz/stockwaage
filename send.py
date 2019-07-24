#!/usr/bin/env python

import sys
import ConfigParser
import socket
from datetime import datetime
import os
import json
from influxdb import InfluxDBClient

dir_path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.read(dir_path + '/config.ini')

data_array = {'weight','temp','humidity'}

def printdebug( text ):
    if config.getboolean('MAIN','DEBUG'):
        print text

def toFile (metric,data):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = dir_path + '/' + metric + '.txt'
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def fromFile (metric):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = dir_path + '/' + metric + '.txt'
    try:
        with open(filename) as json_file:
            data = json.load(json_file)
    except:
        data = {}
        data['weight'] = []
        data['temp'] = []
        data['humidity'] = []

    return data

def clearFile (metrix):
    data = {}
    data['weight'] = []
    data['temp'] = []
    data['humidity'] = []
    toFile(metric,data)

def send (metric):
    influx_server = config.get('INFLUX','SERVER')
    influx_port = config.get('INFLUX','PORT')
    influx_user = config.get('INFLUX','USER')
    influx_password = config.get('INFLUX','PASSWORD')
    influx_database = config.get('INFLUX','DATABASE')
    try:
        dbclient = InfluxDBClient(influx_server, influx_port, influx_user, influx_password, influx_database)

        data = fromFile(metric)
        success = True
        for name in data_array:
            printdebug(name)

            for value in data[name]:
	        json_body = [
                    {
		        "measurement": value['measurement'],
                        "time": value['time'],
                        "fields": {
                            name: value['fields'][name]
                        }
                    }
                ]
	        printdebug(json_body)
	        success = success and dbclient.write_points(json_body)

    except:
        success = False
        printdebug("can not connect to influxdb")

    if success:
        printdebug("success")
	clearFile(metric)

    return

if len(sys.argv) is not 2:
    print "geben Sie bitte eine Metric an !!"
    exit(1)
else:
    metric = sys.argv[1]
    send(metric)
    exit(0)
