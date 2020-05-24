# weatherstation

Based in this tutorial:
https://iada.nl/en/blog/article/temperature-monitoring-raspberry-pi


# rasp-config

In Interfacing Options, enable IC2

``` bash

sudo raspi-config

```


# Install

``` bash

sudo ./install.sh

```

 
# prepare boot config

Add the lines to the file /boot/config.txt

``` ini

dtoverlay=w1-gpio
dtoverlay=gpio-ir-tx,gpio_pin=27
dtoverlay=lirc-rpi

```


RECOMENDED:
``` bash

# system monitor
sudo apt-get install sysstat

# backup file
sudo git clone https://github.com/andreafabrizi/Dropbox-Uploader.git &&  cd Dropbox-Uploader/ && ./dropbox_uploader.sh && ./dropbox_uploader.sh list
sudo crontab -e

# normalize music
sudo apt-get install vbrfix normalize-audio
find /media/usb/mp3 -name "*.mp3" -exec vbrfix -makevbr -always {} {} \; -exec normalize-audio -b {} \;
```

add this line to the root crontab for the backup (RECOMENDED step required)

``` bash
@daily $(sudo -u smarthomelight bash -c 'source $HOME/.smarthomelight && echo $SMARTHOME_DIR')/bin/backup.sh

```


TODO:
https://certbot.eff.org/lets-encrypt/debianwheezy-apache

Using: 

Tornado (REST): http://www.tornadoweb.org/en/stable/

Google Charts: https://developers.google.com/chart/

Better Check Boxes: https://tutorialzine.com/2011/03/better-check-boxes-jquery-css

![hardware](/docs/circuit.jpg)
![home screen](/docs/home.jpg)
![weather](/docs/weather.jpg)
![milight](/docs/milight.jpg)
![music](/docs/music.jpg)
![GPIOs](/docs/gpio.jpg)


