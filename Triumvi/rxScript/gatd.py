import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import time
import urllib2
import json

import triumvi

GATD_URL = 'http://post.gatd.io/0408e009-bef2-4b5b-b4fe-df0b9e3c7a2a'


def postDataToGATD(packet):
    req = urllib2.Request(GATD_URL)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(packet.dictionary))

def callback (pkt):
    for key in pkt._DISPLAYORDER:
        if key in pkt.dictionary:
            print('{0}: {1}'.format(key, pkt.dictionary[key]))
    print('')

    postDataToGATD(pkt)

triumvi.triumvi(callback)
