#!/usr/bin/env python

import random
import sys
import ConfigParser
import socket
import paho.mqtt.publish as publish
from datetime import datetime
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.read(dir_path + '/config.ini')

def stristr ( haystack, needle ):
    pos = haystack.upper().find(needle.upper())
    if pos < 0: # not found
        return None
    else:
        return haystack[pos:]

def getFirstPart (text, char):
    if stristr(text, char):
        retour = text.split(char)[0]
        return retour
    else:
        return text

def getWeight ():
    # test with random 1 to 10
    retour = random.randint(1, 10)
    # in future get weight from hx711
    return retour

def sendWeight (metric, weight):
    # test: print out
    #print metric, ":", weight
    # future: send to mqtt
    hostname = getFirstPart(socket.gethostname(),'.')
    mqtt_server = config.get('MQTT','SERVER')
    mqtt_port = config.get('MQTT','PORT')
    mqtt_keepalive = config.get('MQTT','KEEPALIVE')
    mqtt_path = hostname + "/weight/" + metric
    #print hostname, mqtt_server, mqtt_port, mqtt_keepalive, mqtt_path
    #print datetime.now()
    message = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "|" + str(weight)
    #print message
    publish.single(mqtt_path, message, hostname=mqtt_server)
    return

if len(sys.argv) is not 2:
    print "geben Sie bitte eine Metric an !!"
    exit(1)
else:
    metric = sys.argv[1]
    sendWeight(metric,getWeight())
    exit(0)
