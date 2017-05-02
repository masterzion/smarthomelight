#!/usr/bin/python

import os
import os.path
from shutil import copyfile

CRON_PREFIX="ROOMBA_"
ROOMBA_CRON_DIR="../cron/"
ETC_CRON_DIR="/etc/cron.d/"


for file in os.listdir(ROOMBA_CRON_DIR):
    target_file=ETC_CRON_DIR+CRON_PREFIX + file
    source_file=ROOMBA_CRON_DIR+file

    print target_file

   
    if os.path.exists(target_file):
        print "Y"
        os.remove(target_file)
    else:
        print "N"
        copyfile(source_file, target_file)





