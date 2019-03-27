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

def weightToFile (metric,data):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = dir_path + '/' + metric + '.txt'
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def weightsFromFile (metric):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = dir_path + '/' + metric + '.txt'
    try:
        with open(filename) as json_file:
            data = json.load(json_file)
    except:
        data = {}
        data['weights'] = []
    return data

def clearFile (metrix):
    data = {}
    data['weights'] = []
    weightToFile(metric,data)

def sendWeight (metric):
    influx_server = config.get('INFLUX','SERVER')
    influx_port = config.get('INFLUX','PORT')
    influx_user = config.get('INFLUX','USER')
    influx_password = config.get('INFLUX','PASSWORD')
    influx_database = config.get('INFLUX','DATABASE')
    dbclient = InfluxDBClient(influx_server, influx_port, influx_user, influx_password, influx_database)

    data = weightsFromFile(metric)
    success = True
    for weight in data['weights']:
	json_body = [
            {
		"measurement": weight['measurement'],
                "time": weight['time'],
                "fields": {
                    "weight": weight['fields']['weight']
                }
            }
        ]
	#print json_body
	success = success and dbclient.write_points(json_body)

    if success:
	clearFile(metric)

    return

if len(sys.argv) is not 2:
    print "geben Sie bitte eine Metric an !!"
    exit(1)
else:
    metric = sys.argv[1]
    sendWeight(metric)
    exit(0)
