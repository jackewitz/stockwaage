# Projekt digitale Stockwaage

## Client (Stockwaage)

Der Client, d.h. die eigentliche Stockwaage, basiert auf:

* Raspberry Pi Zero WH
* HX711 + 4 Wägenzellen (Gewicht)
* DHT22 (Temperatur, Luftfeuchtigkeit)

Die zugehörigen Python-Scripte finden sich hier.

### cron jobs
Um Daten zu sammeln und Daten an den Server zu senden, werden cron jobs verwendet.

    sudo nano /etc/crontab

Bitte einfügen:

    # save data
    #* *     * * *   pi      /home/pi/stockwaage/save.py 1m
    */10 *  * * *   pi      /home/pi/stockwaage/save.py 10m
    0 *     * * *   pi      /home/pi/stockwaage/save.py 1h
    0 0     * * *   pi      /home/pi/stockwaage/save.py 1d

    # send data
    15 8     * * *   pi      /home/pi/stockwaage/send.sh
    15 12     * * *   pi      /home/pi/stockwaage/send.sh
    15 16     * * *   pi      /home/pi/stockwaage/send.sh
    15 20     * * *   pi      /home/pi/stockwaage/send.sh

Das Interval von einer Minute (1m) ist zu kurz für den Pi Zero, da der cron job länger als eine Minute braucht. Von daher nur zu Testzwecken aktivieren.

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
