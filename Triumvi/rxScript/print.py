import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import time

import triumvi

def callback (pkt):
    for key in pkt._DISPLAYORDER:
        if key in pkt.dictionary:
            print('{0}: {1}'.format(key, pkt.dictionary[key]))
    print('')

triumvi.triumvi(callback)
