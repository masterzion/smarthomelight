#!/bin/bash

cd /root/Dropbox-Uploader/

export USR_HOME=$(sudo -u smarthomelight bash -c 'echo $HOME')/
export SMARTHOME_DIR=$(sudo -u smarthomelight bash -c 'source $HOME/.smarthomelight && echo $SMARTHOME_DIR')

./dropbox_uploader.sh upload /etc/mpd.conf bkp_raspberry/mpd.conf
./dropbox_uploader.sh upload /etc/lirc bkp_raspberry/
./dropbox_uploader.sh upload /boot/config.txt bkp_raspberry/config.txt
./dropbox_uploader.sh upload /etc/mpdscribble.conf bkp_raspberry/mpdscribble.conf
./dropbox_uploader.sh upload /var/lib/mpd/playlists bkp_raspberry/
./dropbox_uploader.sh upload $USR_HOME/.smarthomelight bkp_raspberry/.smarthomelight
./dropbox_uploader.sh upload $SMARTHOME_DIR/modules/tuya/tuya.conf bkp_raspberry/tuya.conf
./dropbox_uploader.sh upload $SMARTHOME_DIR/modules/weatherstation/db/smarthome.db bkp_raspberry/smarthome.db
./dropbox_uploader.sh upload /etc/transmission-daemon/settings.json bkp_raspberry/
