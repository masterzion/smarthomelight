#!/usr/bin/python
import time

from models import Sensors

while True:
    print Sensors().getLast()
    time.sleep(5)

