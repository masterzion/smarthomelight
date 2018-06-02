# weatherstation

Based in this tutorial:
https://iada.nl/en/blog/article/temperature-monitoring-raspberry-pi


INSTALL
``` bash
apt-get install python-setuptools git sqlite3 python-smbus i2c-tools arp-scan

git clone git://git.drogon.net/wiringPi
cd wiringPi
./build


echo i2c-dev >> /etc/modules
modprobe i2c-dev

easy_install pip
pip install tornado w1thermsensor pyping milight RPi.GPIO

git clone https://github.com/masterzion/weatherstation.git
cd weatherstation
``` 

add this line in  /boot/config.txt
``` ini
dtoverlay=w1-gpio
```


Set the variables in .bashrc file

``` bash
SMARTHOME_DIR=/root/weatherstation
SMARTHOME_LOCKDIR="$SMARTHOME_DIR/lockfiles"
FILE="$SMARTHOME_LOCKDIR/houseisempt.lock"

MAC_LIST="AA:BB:CC:DD:EE:FF AA:BB:CC:DD:EE:FF"

SERVER_NAME="pass@localhost" 
SERVER_PORT="6600"

MILIGHT_MAC="AA:BB:CC:DD:EE:FF"
MILIGHT_PORT="milight_port"
MILIGHT_GROUP="1"

export WEATHER_SERVER_PWD='WEB_PASSWORD'
export WEATHER_SERVER_SALT='add some random chars here'

export FILE_CINEMAMODE="$SMARTHOME_LOCKDIR/cinemamode.lock"
```

add the crontabfile content in your crontab and reboot

RECOMENDED:
``` bash
  apt-get install sysstat
```

TODO:
https://certbot.eff.org/lets-encrypt/debianwheezy-apache

Using: 

Tornado (REST): http://www.tornadoweb.org/en/stable/

Google Charts: https://developers.google.com/chart/



Online Sample:

http://masterzion.no-ip.org:8888/
