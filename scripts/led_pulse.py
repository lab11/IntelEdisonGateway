#!/usr/bin/env python

import EdisonGatewayLEDs
import time

e = EdisonGatewayLEDs.EdisonGatewayLEDs()

i = 0
up = True
while True:
	if up:
		i += 1
	else:
		i -= 1

	# set_pwm(PWM_BLUE, i)
	e.on(EdisonGatewayLEDs.LED_BLUE, i)

	if i == 100:
		up = False
	elif i == 0:
		up = True

	time.sleep(0.01)
