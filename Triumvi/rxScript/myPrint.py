import sys
import datetime
import signal
from collections import defaultdict
from d2cMsgSender import D2CMsgSender
import json

sys.path.append('/usr/local/lib/python2.7/site-packages')
import time

import triumvi
src_dict = {}

ALLOW_DEVICES = set()
f = open('ALLOWED_DEVICES.txt', 'r')
for line in f:
    tmp = line.split()
    if len(tmp) > 0:
        ALLOW_DEVICES.add(tmp[0])
f.close()
if len(ALLOW_DEVICES) > 0:
    print('Receving packets from the following Triumvis: ')
    for d in ALLOW_DEVICES:
        print('{:}'.format(d))
else:
    print('Receving packets from all Triumvis')
    

# Azure instance 
connectionString = 'HostName=Triumvi.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=G0+S2qWEodiVTxmBVJsxU+5yY7E6LZVYNG6B2gyy0R0='
d2cMsgSender = D2CMsgSender(connectionString)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def signal_handler(signal, frame):
    sys.exit(0)

def colorPrint(myStr, color):
    print(color + myStr + bcolors.ENDC)


def callback (pkt):
    global src_dict
    device_id = pkt.dictionary['_meta']['device_id']
    if 'phase offset' in pkt.dictionary:
        print('Device ID: {:}'.format(device_id))
        print('Phase Offset: {:}'.format(pkt.dictionary['phase offset']))
        print('DC Offset: {:}'.format(pkt.dictionary['dc offset']))
        for key in pkt.dictionary['data'].keys():
            iSlope = float(pkt.dictionary['data'][key][0])/pkt.dictionary['data'][key][1]
            pSlope = float(pkt.dictionary['data'][key][3])/pkt.dictionary['data'][key][4]
            if iSlope > 1.1 or iSlope < 0.9 or pSlope > 1.1 or pSlope < 0.9:
                colorPrint('Outlier calibration coefficients, re-calibration required!', bcolors.FAIL)
            print('INA Gain Idx: {:}'.format(key))
            colorPrint('Current Fit, Slope: {:.2f}, Offset: {:}'.format(iSlope, pkt.dictionary['data'][key][2]), bcolors.WARNING)
            colorPrint('Power Fit, Slope: {:.2f}, Offset: {:}'.format(pSlope, pkt.dictionary['data'][key][5]), bcolors.WARNING)
            print('DC Offset: {:}\n\n'.format(pkt.dictionary['data'][key][6]))
    elif 'Power' in pkt.dictionary and (len(ALLOW_DEVICES)==0 or (pkt.dictionary['Power'] > 30 or device_id[-2:] in ALLOW_DEVICES)):
        time_str = ''
        if 'Time Stamp' in pkt.dictionary:
            time_str = str(pkt.dictionary['Time Stamp'])
        else:
            time_str = str(datetime.datetime.now())
        if device_id not in src_dict:
            src_dict[device_id] = set()

        if time_str not in src_dict[device_id]:
            # Azure 
            ##message = json.dumps({"power": pkt.dictionary['Power'], \
            ##    "powerFactor": pkt.dictionary['Power Factor'], \
            ##    "DeviceID":device_id})
            ##AzureDeviceId = device_id;
            ##d2cMsgSender.sendD2CMsg(AzureDeviceId, message)
            # end of Azure
            print('Device ID: {:}'.format(device_id[:-4])),
            colorPrint('{:}'.format(device_id[-4:]), bcolors.FAIL)
            print('Packet Counted by Gateway: {0}'.format(len(src_dict[device_id])))
            if 'RSSI' in pkt.dictionary:
                colorPrint('RSSI: {:} dBm'.format(pkt.dictionary['RSSI']), bcolors.OKGREEN)
            src_dict[device_id].add(time_str)
            for key in pkt._DISPLAYORDER:
                if key in pkt.dictionary:
                    if key=='Time Stamp':
                        colorPrint('RTC time stamp: {:}'.format(pkt.dictionary['Time Stamp']), bcolors.WARNING)
                    elif key=='Power' or key=='IRMS':
                        colorPrint('{0}: {1}'.format(key, pkt.dictionary[key]), bcolors.OKGREEN)
                    else:
                        print('{0}: {1}'.format(key, pkt.dictionary[key]))
            print('')


signal.signal(signal.SIGINT, signal_handler)
myTriumvi = triumvi.triumvi(callback)

