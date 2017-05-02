# weatherstation

Based in this tutorial:
https://iada.nl/en/blog/article/temperature-monitoring-raspberry-pi


INSTALL
``` bash
apt-get install python-setuptools git sqlite3 python-smbus i2c-tools

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
MOBILE_IP="mobile_Ip"
SERVER_NAME="pass@localhost" 
SERVER_PORT="6600"

MILIGHT_IP="milight_IP"
MILIGHT_PORT="milight_port"
MILIGHT_GROUP="1"
```


add the crontabfile content in your crontab and reboot


Using: 

Tornado (REST): http://www.tornadoweb.org/en/stable/

Google Charts: https://developers.google.com/chart/



Online Sample:

http://masterzion.no-ip.org:8888/
