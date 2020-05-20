# weatherstation

Based in this tutorial:
https://iada.nl/en/blog/article/temperature-monitoring-raspberry-pi


# Install dependences

``` bash
sudo apt-get install python-setuptools python-pip python-dev build-essential git sqlite3 python-smbus i2c-tools arp-scan bc git screen mpd mpc authbind mpdscribble
sudo pip install tornado w1thermsensor pyping milight RPi.GPIO Adafruit_DHT pytuya

git clone https://github.com/masterzion/WiringPi.git
cd WiringPi
./build
cd


sudo raspi-config
```
In Interfacing Options, enable IC2



# Configure the environment:

``` bash
sudo mkdir /media/usb
sudo echo "/dev/sda1 /media/usb/ ntfs none 0 0" >> /dev/fstab
sudo mount -a

cd /opt
sudo git clone https://github.com/masterzion/smarthomelight.git
sudo useradd -m smarthomelight -s /bin/bash
sudo cp /home/pi/.bashrc  /opt/smarthomelight/.bashrc
sudo chown -R smarthomelight smarthomelight
sudo usermod -a -G i2c smarthomelight
sudo usermod -a -G gpio smarthomelight

sudo touch /etc/authbind/byport/80
sudo chmod 700 /etc/authbind/byport/80
sudo chown smarthomelight /etc/authbind/byport/80
sudo cp /opt/smarthomelight/cron_smarthomelight /etc/cron.d/
sudo crontab -u smarthomelight /opt/smarthomelight/smartcron/00000_do_not_remove
sudo chmod 775 /opt/smarthomelight/modules/weatherstation/db
sudo mkdir /opt/smarthomelight/modules/weatherstation/db
sudo chown smarthomelight:smarthomelight /opt/smarthomelight/modules/weatherstation/db

touch /opt/smarthomelight/modules/webserver/home/js/day.json
chmod 765 /opt/smarthomelight/modules/webserver/home/js/day.json
chown smarthomelight:smarthomelight /opt/smarthomelight/modules/webserver/home/js/day.json
``` 

Add the lines to the file /boot/config.txt

``` ini

dtoverlay=w1-gpio
dtoverlay=gpio-ir-tx,gpio_pin=27
dtoverlay=lirc-rpi

```


Create the variables ~/.smarthomelight 

``` bash

export SMARTHOME_DIR=/opt/smarthomelight
export SMARTHOME_LOCKDIR="/tmp/"
export SMARTHOME_MEMDB_PORT=3030

export MAC_LIST="AA:BB:CC:DD:EE:FF AA:BB:CC:DD:EE:FF"

export SERVER_NAME="pass@localhost"
export SERVER_PORT="6600"

export MILIGHT_MAC="AA:BB:CC:DD:EE:FF"
export MILIGHT_PORT="8899"
export MILIGHT_GROUP="1"

export CHROMECAST_MAC="AA:BB:CC:DD:EE:FF"

export IFACE=eth0

export GPIO=/usr/local/bin/gpio

export WEATHER_SERVER_PWD='WEB_PASSWORD'
export WEATHER_SERVER_SALT='add some random chars here'

export FILE_CINEMAMODE="$SMARTHOME_LOCKDIR/cinemamode.lock"

```

Add it to the ~/.bashrc file

``` bash

source ~/.smarthomelight

``` 

add to /etc/sudoers

``` ini

smarthomelight ALL= NOPASSWD: /usr/sbin/arp-scan

```



RECOMENDED:
``` bash

# system monitor
apt-get install sysstat

# backup file
sudo git clone https://github.com/andreafabrizi/Dropbox-Uploader.git &&  cd Dropbox-Uploader/ && ./dropbox_uploader.sh && ./dropbox_uploader.sh list
sudo crontab -e

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

![hardware](/docs/circuit.jpg)
![home screen](/docs/home.jpg)
![weather](/docs/weather.jpg)
![milight](/docs/milight.jpg)
![music](/docs/music.jpg)



