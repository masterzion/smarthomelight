#!/bin/bash

echo ##########################
echo INTALLING ALL DEPENDENCES
echo ##########################

apt-get install -y  python3-setuptools python3-pip python3-dev python3
apt-get install -y  build-essential git sqlite3 python3-smbus i2c-tools arp-scan bc git screen mpd mpc authbind mpdscribble bpm-tools miniupnpc libgpiod-dev:armhf wildmidi
pip3 install --no-input tornado w1thermsensor pyping milight RPi.GPIO Adafruit_DHT pytuya adafruit_dht

git clone https://github.com/masterzion/WiringPi.git
cd WiringPi
./build
cd ..
rm -rf WiringPi


echo ##########################
echo Preparing the environment
echo ##########################

echo ':msg, contains, "device eth1 entered promiscuous mode"   ~' >> /etc/rsyslog.d/zz-promiscuous.conf
echo ':msg, contains, "device eth1 left promiscuous mode"      ~' >> /etc/rsyslog.d/zz-promiscuous.conf
service rsyslog restart


mkdir -p /opt/smarthomelight
cp -rf * /opt/smarthomelight

cd /opt/smarthomelight
useradd -m smarthomelight -s /bin/bash
cp /home/pi/.bashrc  /opt/smarthomelight/.bashrc
chown smarthomelight:smarthomelight /opt/smarthomelight/.bashrc
cp .smarthomelight /opt/smarthomelight/.smarthomelight
chown smarthomelight:smarthomelight /opt/smarthomelight/.smarthomelight
chmod -w /opt/smarthomelight/.smarthomelight
echo 'source ~/.smarthomelight' >> /home/pi/.bashrc
echo 'smarthomelight ALL= NOPASSWD: /usr/sbin/arp-scan' >> /etc/sudoers

usermod -a -G i2c smarthomelight
usermod -a -G gpio smarthomelight

touch /etc/authbind/byport/80
chmod 700 /etc/authbind/byport/80
chown smarthomelight /etc/authbind/byport/80
cp /opt/smarthomelight/cron_smarthomelight /etc/cron.d/
crontab -u smarthomelight /opt/smarthomelight/smartcron/00000_do_not_remove
chmod 775 /opt/smarthomelight/modules/weatherstation/db
mkdir /opt/smarthomelight/modules/weatherstation/db
chown smarthomelight:smarthomelight /opt/smarthomelight/modules/weatherstation/db

touch /opt/smarthomelight/modules/webserver/home/js/day.json
chmod 765 /opt/smarthomelight/modules/webserver/home/js/day.json
chown smarthomelight:smarthomelight /opt/smarthomelight/modules/webserver/home/js/day.json

echo ##########################
echo Add external drive
echo ##########################

read -p "Add '/dev/sda1 /media/usb/ ntfs none 0 0' to the fstab?" -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
  mkdir /media/usb
  echo "/dev/sda1 /media/usb/ ntfs none 0 0" >> /dev/fstab
  mount -a
fi

echo * IMPORTANT: Please validate the configuration at the file:
echo /opt/smarthomelight/.smarthomelight

