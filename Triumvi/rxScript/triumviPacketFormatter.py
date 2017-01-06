
from datetime import datetime
import uuid

gateway_id = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])

def unpack(data):
    return float(data[0] + (data[1]<<8) + (data[2]<<16) + (data[3]<<24))

class triumviPacket(object):
    def __init__(self, data):
        self.dictionary = {}

        self._TRIUMVI_PKT_ID = 160
        self._AES_PKT_ID = 120
        self._DISPLAYORDER = \
        ['Packet Type', 'Source Addr', 'Power', \
        'External Voltage Waveform', 'Battery Pack Attached', 'Three Phase Unit', \
        'Frame Write', 'Panel ID', 'Circuit ID', 'Power Factor', 'VRMS', 'IRMS', 'INA Gain']

        if data[0] == self._TRIUMVI_PKT_ID:
            self.dictionary['Packet Type'] = 'Triumvi Packet'
        elif data[0] == self._AES_PKT_ID:
            self.dictionary['Packet Type'] = 'Old Triumvi Packet'
        else:
            return None

        # self.dictionary['Source Addr'] = [hex(i) for i in data[1:9]]
        device_id = ''.join(['{:02x}'.format(i) for i in data[1:9]])
        self.dictionary['Power'] = unpack(data[9:13])/1000
        offset = 14
        if self.dictionary['Packet Type'] == 'Triumvi Packet':
            if data[13] & 128:
                self.dictionary['External Voltage Waveform'] = True
            if data[13] & 64:
                self.dictionary['Battery Pack Attached'] = True
                self.dictionary['Panel ID'] = data[offset]
                self.dictionary['Circuit ID'] = data[offset+1]
                offset += 2
            if data[13] & 48:
                self.dictionary['Three Phase Unit'] = True
            if data[13] & 8:
                self.dictionary['Fram Write'] = True
            if data[13] & 4:
                self.dictionary['Power Factor'] = unpack(data[offset:offset+2]+[0,0])/1000
                self.dictionary['VRMS'] = data[offset+2]
                self.dictionary['IRMS'] = unpack(data[offset+4:offset+6]+[0,0])/1000
                self.dictionary['INA Gain'] = data[offset+3]
            if data[13] & 2:
                self.dictionary['Time Stamp'] = datetime(\
                    data[offset+6]+2000, \
                    data[offset+7], \
                    data[offset+8], \
                    data[offset+9], \
                    data[offset+10], \
                    data[offset+11])

        self.dictionary['_meta'] = {
            'received_time': datetime.utcnow().isoformat(),
            'gateway_id': gateway_id,
            'receiver': 'cc2538',
            'device_id': device_id
        }
        self.dictionary['device'] = 'Triumvi'

    def addTimeStamp(self, timeStamp):
        self.dictionary['Time Stamp'] = {\
            'Year':timeStamp.year, \
            'Month':timeStamp.month, \
            'Day:':timeStamp.day, \
            'Hour':timeStamp.hour, \
            'Minute':timeStamp.minute, \
            'Second':timeStamp.second }

