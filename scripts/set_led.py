#!/usr/bin/env python

import EdisonGatewayLEDs

import sys
import time

if len(sys.argv) != 3:
	print('USAGE: {} <red|green|blue> <brightness 0-100>'.format(sys.argv[0]))
	sys.exit(1)

color = sys.argv[1]
color_val = EdisonGatewayLEDs.LED_RED
if color == 'red': color_val = EdisonGatewayLEDs.LED_RED
elif color == 'green': color_val = EdisonGatewayLEDs.LED_GREEN
elif color == 'blue': color_val = EdisonGatewayLEDs.LED_BLUE
else:
	print('Invalid color')
	sys.exit(1)

try:
	brightness = int(sys.argv[2])
	if brightness < 0: brightness = 0
	if brightness > 100: brightness = 100
except:
	print('Invalid brightness')
	sys.exit(1)

e = EdisonGatewayLEDs.EdisonGatewayLEDs()

e.on(color_val, brightness)
