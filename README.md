# weatherstation

Based in this tutorial:
https://iada.nl/en/blog/article/temperature-monitoring-raspberry-pi


INSTALL
``` bash
sudo apt-get install python-setuptools python-pip python-dev build-essential git sqlite3 python-smbus i2c-tools arp-scan bc git screen mpd mpc authbind

sudo raspi-config
```

In Interfacing Options, enable IC2



``` bash
sudo pip install tornado w1thermsensor pyping milight RPi.GPIO Adafruit_DHT pytuya

git clone https://github.com/masterzion/WiringPi.git
cd WiringPi
./build
cd

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

sudo raspi-config
``` 
In Interfacing Options, enable IC2



add this line in  /boot/config.txt
``` ini
dtoverlay=w1-gpio
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


add the crontabfile content in your crontab and reboot

``` bash
@reboot [SMARTHOME_DIR]/bin/service_manager.sh start autostart start_modules
```

add to /etc/sudoers

``` bash
smarthomelight ALL= NOPASSWD: /usr/sbin/arp-scan

```


RECOMENDED:
``` bash
  apt-get install sysstat
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



