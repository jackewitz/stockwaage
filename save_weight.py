#!/usr/bin/env python

import random
import sys
import ConfigParser
import socket
from datetime import datetime
import os
import json

import RPi.GPIO as GPIO
import time
from hx711 import HX711
hx = HX711(5, 6)

dir_path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.read(dir_path + '/config.ini')

def hx711_setup():
    GPIO.setwarnings(False)
    hx.set_offset(float(config.get('HX711','OFFSET')))
    hx.set_scale(float(config.get('HX711','SCALE')))
    pass

def hx711_get():
    retour = 0
    sum = 0;
    hx711_setup()
    for x in range(10):
        val = hx.get_grams()
        sum = sum + val
        #print val

        hx.power_down()
        time.sleep(.001)
        hx.power_up()

    GPIO.cleanup()
    #print sum
    retour = max(0, int(round(sum / 10)))
    #print retour

    return retour

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
    #retour = random.randint(1, 10)
    # in future get weight from hx711
    retour = hx711_get()
    return retour

def saveWeight (metric, weight):
    hostname = getFirstPart(socket.gethostname(),'.')
    topic = hostname + "/weight/" + metric
    data = weightsFromFile(metric)
    data['weights'].append({
        "measurement": topic,
        "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "fields": {
            "weight": weight
        }
    })
    weightToFile(metric,data)
    return

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

if len(sys.argv) is not 2:
    print "geben Sie bitte eine Metric an !!"
    exit(1)
else:
    metric = sys.argv[1]
    saveWeight(metric,getWeight())
    exit(0)

