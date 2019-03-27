#!/usr/bin/env python

import random
import sys
import socket
from datetime import datetime
import os
import json

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

