#!/bin/bash

LIST_HOME=/var/lib/mpd/playlists/
MP3_HOME=/media/usb/mp3/
while read line; do
# reading each line
cp "$MP3_HOME$line" "$2"
done < "$LIST_HOME$1.m3u"
