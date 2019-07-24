#!/usr/bin/env python

import random
import sys
import ConfigParser
import socket
from datetime import datetime
import os
import json

#import RPi.GPIO as GPIO
#import time
#from hx711 import HX711
#hx = HX711(5, 6)

#import Adafruit_DHT

dir_path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.read(dir_path + '/config.ini')

if config.getboolean('HX711','SAVE'):
    import RPi.GPIO as GPIO
    import time
    from hx711 import HX711
    hx = HX711(5, 6)
if config.getboolean('DHT22','SAVE'):
    import Adafruit_DHT

def printdebug( text ):
    if config.getboolean('MAIN','DEBUG'):
        print text

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
        printdebug(val)

        hx.power_down()
        time.sleep(.001)
        hx.power_up()

    GPIO.cleanup()
    printdebug(sum)
    retour = max(0, int(round(sum / 10)))
    printdebug(retour)

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

def saveData (name, metric, value):
    hostname = getFirstPart(socket.gethostname(),'.')
    topic = hostname + "/" + name + "/" + metric
    data = fromFile(metric)
    data[name].append({
        "measurement": topic,
        "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "fields": {
            name: value
        }
    })
    toFile(metric,data)
    return

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

if len(sys.argv) is not 2:
    print "geben Sie bitte eine Metric an !!"
    exit(1)
else:
    metric = sys.argv[1]
    if config.getboolean('HX711','SAVE'):
        printdebug("HX711")
        saveData('weight',metric,getWeight())
    if config.getboolean('DHT22','SAVE'):
        printdebug("DHT22")

        #Sensortyp und GPIO festlegen
        sensor = Adafruit_DHT.DHT22
        gpio = 4

        # Daten auslesen und speichern
        humidity = 200.0
        temperature = 200.0
        while humidity < 0 or humidity > 100 or temperature < -40 or temperature > 80:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
            printdebug(round(temperature, 1))
            printdebug(round(humidity, 1))

        saveData('temp',metric,round(temperature, 1))
        saveData('humidity',metric,round(humidity, 1))

        # Ausgabe
        printdebug('Temperatur: {0:0.1f}*C Luftfeuchtigkeit: {1:0.1f}%'.format(temperature,humidity))

    exit(0)

