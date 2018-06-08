#!/usr/bin/python
import json

from models import Sensors

print json.dumps( Sensors().getDay() )


