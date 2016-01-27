#!/usr/bin/env python

import EdisonGatewayLEDs

import sys
import time

if len(sys.argv) != 2:
	print('USAGE: {} <hex code>'.format(sys.argv[0]))
	sys.exit(1)

color = sys.argv[1]

e = EdisonGatewayLEDs.EdisonGatewayLEDs()
e.hex(color)
