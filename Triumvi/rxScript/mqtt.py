import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import time
import urllib2
import json

import triumvi

import paho.mqtt.client as mqtt




def callback (pkt):
    print(json.dumps(pkt.dictionary))
    # for key in pkt._DISPLAYORDER:
    #     if key in pkt.dictionary:
    #         print('{0}: {1}'.format(key, pkt.dictionary[key]))
    # print('')

    # postDataToGATD(pkt)
    client.publish('gateway-data', json.dumps(pkt.dictionary))
    # client.publish('hi', 'there')


client = mqtt.Client()
client.connect('141.212.11.163', 1883, 60)

triumvi.triumvi(callback)
