#!/usr/bin/env python3
#
# This is a NetworkTables client (eg, the DriverStation/coprocessor side).
# You need to tell it the IP address of the NetworkTables server (the
# robot or simulator).
#
# When running, this will continue incrementing the value 'dsTime', and the
# value should be visible to other networktables clients and the robot.
#

import sys
import time
from networktables import NetworkTable, NumberArray

# To see messages from networktables, you must setup logging
import logging
logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) != 2:
    print("Error: specify an IP to connect to!")
    exit(0)

ip = sys.argv[1]

NetworkTable.setIPAddress(ip)
NetworkTable.setClientMode()
NetworkTable.initialize()

sd = NetworkTable.getTable("/GRIP/myContoursReport")
na = NumberArray()
#sna.append(1)

#sd.putValue('centerX', na)

i = 0

while True:
    try:
        ret = sd.retrieveValue("centerX", na)
        print(ret, na)
    except KeyError:
        print('centerX: N/A')

    time.sleep(1)
    i += 1

