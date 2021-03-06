# Projekt digitale Stockwaage

## Client (Stockwaage)

Der Client, d.h. die eigentliche Stockwaage, basiert auf:

* Raspberry Pi Zero WH
* HX711 + 4 Wägenzellen (Gewicht)
* DHT22 (Temperatur, Luftfeuchtigkeit)

Die zugehörigen Python-Scripte finden sich hier.

### DHT22 (Temperatur, Luftfeuchtigkeit)

Zur Nutzung des DHT22 wird eine Python Bibliothek von Adafruit benutzt. Diese muss zunächst installiert werden.

Voraussetzungen:

    sudo apt-get update
    sudo apt-get install build-essential python-dev python-openssl

Installation:

    git clone https://github.com/adafruit/Adafruit_Python_DHT.git
    cd Adafruit_Python_DHT
    sudo python setup.py install

Test:

    cd examples
    sudo ./AdafruitDHT.py 22 4

* 22 = Typ (11 oder 22)
* 4 = GPIO

Optional:

    sudo nano /boot/config.txt
    dtoverlay=dht11,gpiopin=4

Quelle: https://www.einplatinencomputer.com/raspberry-pi-temperatur-und-luftfeuchtigkeitssensor-dht22/

### cron jobs
Um Daten zu sammeln und Daten an den Server zu senden, werden cron jobs verwendet.

    sudo nano /etc/crontab

Bitte einfügen:

    # save data
    #* *     * * *   pi      /home/pi/stockwaage/save.sh 1m
    */10 *  * * *   pi      /home/pi/stockwaage/save.sh 10m
    0 *     * * *   pi      /home/pi/stockwaage/save.sh 1h
    0 0     * * *   pi      /home/pi/stockwaage/save.sh 1d

    # send data
    15 8     * * *   pi      /home/pi/stockwaage/send.sh
    15 12     * * *   pi      /home/pi/stockwaage/send.sh
    15 16     * * *   pi      /home/pi/stockwaage/send.sh
    15 20     * * *   pi      /home/pi/stockwaage/send.sh

Die Messpunkte pro Minute erzeugen sehr viele Daten und sind daher nur zum Testen gedacht.

### Konfiguration

Kopieren der Datei `config.ini-dist` nach `config.ini`:

    [MAIN]
    DEBUG = True
    WLAN = ON
    ACTIVE = False
    CRON = OFF

* DEBUG = True (mit Ausgaben auf der Konsole) oder False (ohne Ausgaben)
* WLAN = ON (bleibt an) oder OFF (wird 10 Minuten nach dem Senden der Werte ausgeschaltet)
* ACTIVE = True (es wird gemessen) oder False (es wird nicht gemessen)
* CRON = ON (die Cronjobs sind aktiv) oder OFF (cronjobs inaktiv)

#### Produktion
    [MAIN]
    DEBUG = False
    WLAN = OFF
    ACTIVE = True
    CRON = ON

#### Debugging / Development
    [MAIN]
    DEBUG = True
    WLAN = ON
    ACTIVE = True
    CRON = OFF

## Server

Der Server, d.h. die Datensammlung und Anzeige, basiert auf:

* Raspberry Pi 3B
* InfluxDB (Zeitreihendatenbank)
* Grafana (Dashboard)

Hierzu hab ich keine Anleitung verfasst, da es davon viele im Netz gibt.

## Versuche

### mqtt

Wenn die Verbindung zum Server weg ist, dann sollen die Werte dennoch zum Server gelangen, wenn die Verbindung wieder steht. Mit MQTT habe ich diese Pufferung nicht hinbekommen.

Jetzt wird per Python zwischen gepuffert bzw. das Design trennt klar zwischen Daten holen / speichern und senden.

Insbesondere wollte ich das WLAN an den Bienenstöcken nur dediziert und selten am Tag anschalten.
