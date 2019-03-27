# stockwaage
Projekt digitale Stockwaage

## cron jobs

    sudo nano /etc/crontab

insert:

    # save weight
    * *     * * *   pi      /home/pi/stockwaage/save_weight.py 1m
    */10 *  * * *   pi      /home/pi/stockwaage/save_weight.py 10m
    0 *     * * *   pi      /home/pi/stockwaage/save_weight.py 1h
    0 0     * * *   pi      /home/pi/stockwaage/save_weight.py 1d

    # send weight
    15 8     * * *   pi      /home/pi/stockwaage/send_weight.sh
    15 12     * * *   pi      /home/pi/stockwaage/send_weight.sh
    15 16     * * *   pi      /home/pi/stockwaage/send_weight.sh
    15 20     * * *   pi      /home/pi/stockwaage/send_weight.sh
