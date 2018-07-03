#!/usr/bin/env python2.7


import pytuya

DEVICE_ID = ''
LOCAL_KEY = ''
IP_ADDRESS= ''


d = pytuya.OutletDevice(DEVICE_ID, IP_ADDRESS, LOCAL_KEY)
data = d.status()  # NOTE this does NOT require a valid key
print('Dictionary %r' % data)
print('state (bool, true is ON) %r' % data['dps']['1'])  # Show status of first controlled switch on device

# Toggle switch state
switch_state = data['dps']['1']
data = d.set_status(not switch_state)  # This requires a valid key
if data:
    print('set_status() result %r' % data)
