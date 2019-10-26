#!/usr/bin/env python

import random
import sys
import ConfigParser
import socket
from datetime import datetime
import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.read(dir_path + '/config.ini')

if config.getboolean('HX711','SAVE'):
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    import time
    from hx711 import HX711
    hx = HX711(5, 6)
if config.getboolean('DHT22','SAVE'):
    import Adafruit_DHT

def printdebug( text ):
    if config.getboolean('MAIN','DEBUG'):
        print text

def hx711_setup():
    hx.set_offset(float(config.get('HX711','OFFSET')))
    hx.set_scale(float(config.get('HX711','SCALE')))
    pass

def hx711_get():
    retour = 0
    val_array = []
    hx711_setup()
    for x in range(10):
        val = hx.get_grams()
        printdebug(val)
        if val > 0:
            val_array.append(val)

        hx.power_down()
        time.sleep(.001)
        hx.power_up()

    if len(val_array) > 0:
        printdebug("gemessene Werte: "+str(val_array))
        val_array = reject_outliers(val_array)
        printdebug("gereinigter Array: "+str(val_array))
        retour = max(0, int(round(sum(val_array) / float(len(val_array)))))

    printdebug("Gewicht: "+str(retour))
    return retour

def quantile(arr, point):
    retour = 0
    length = len(arr)
    pos = length * point
    pos1 = int(abs(pos))
    pos2 = int(abs(pos))+1
    if pos2 >= len(arr):
       pos2 = pos1
    if pos == pos1:
        retour = arr[pos1]
    else:
        retour = (arr[pos1]+arr[pos2])/2
    return retour

def reject_outliers(arr, iq_range=0.6):
    arr.sort()
    pcnt = (1 - iq_range) / 2
    min = quantile(arr, pcnt)
    max = quantile(arr, 1-pcnt)
    printdebug("Array:"+str(arr))
    printdebug("Grenze min: "+str(min))
    printdebug("Grenze max: "+str(max))

    retour = []
    for x in range(len(arr)):
        if arr[x] >= min and arr[x] <= max:
            retour.append(arr[x])
    printdebug("Array bereinigt: "+str(retour))

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

    if config.getboolean('MAIN','ACTIVE'):
        printdebug("Aktive Messung fuer " + metric)

        if config.getboolean('HX711','SAVE'):
            printdebug("HX711")
            saveData('weight',metric,getWeight())
        else:
            printdebug("HX711: ausgeschaltet")

        if config.getboolean('DHT22','SAVE'):
            printdebug("DHT22")

            #Sensortyp und GPIO festlegen
            sensor = Adafruit_DHT.DHT22
            gpio = 4

            # Daten auslesen und speichern
            humidity = 200.0
            temperature = 200.0
            counter = 0
            while humidity < 0 or humidity > 100 or temperature < -40 or temperature > 80:
                counter = counter + 1
                printdebug(str(counter) + ". Messung")
                humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
                if temperature is not None:
                    printdebug(round(float(temperature), 1))
                else:
                    printdebug("Fehler beim Messen der Temperatur")
                if humidity is not None:
                    printdebug(round(float(humidity), 1))
                else:
                    printdebug("Fehler beim Messen der Luftfeuchtigkeit")
                if counter >= 3:
                    break

            if temperature is not None:
                saveData('temp',metric,round(temperature, 1))
            if humidity is not None:
                saveData('humidity',metric,round(humidity, 1))

            # Ausgabe
            if temperature is not None and humidity is not None:
                printdebug('Temperatur: {0:0.1f}*C Luftfeuchtigkeit: {1:0.1f}%'.format(temperature,humidity))
            else:
                printdebug('FEHLER')
        else:
            printdebug('DHT22: ausgeschaltet')

    else:
        printdebug('Messung deaktiviert')

    exit(0)
