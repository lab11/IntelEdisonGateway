#!/usr/bin/env python2

# Do some hacking for the edison and sudo and python and oh my god why
# is this so hard.
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

# System dependencies
import time
import json

# Library for getting data from the CC2538/Triumvi
import triumvi

# MQTT
import paho.mqtt.client as mqtt


# Called on every packet from the Triumvi
def callback (pkt):
	try:
	    json_pkt = json.dumps(pkt.dictionary)
	    client.publish('gateway-data', json_pkt)
	except Exception as e:
		print('Error in callback with Triumvi packet')
		print(e);

# Connect to the local MQTT broker
client = mqtt.Client()
client.connect('localhost', 1883, 60)

# Start getting Triumvi Packets
triumvi.triumvi(callback)
