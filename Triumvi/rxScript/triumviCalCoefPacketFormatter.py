
def unpack(data):
    return data[0] + (data[1]<<8) + (data[2]<<16) + (data[3]<<24)

def convertSign(val):
    return val if val <= 0x7fffffff else val - 0xffffffff

class triumviCalCoefPacketFormatter(object):
    def __init__(self, payload, src_addr):
        self.dictionary = {}
        device_id = ''.join(['{:02x}'.format(i) for i in src_addr])
        self.dictionary['_meta'] = {'device_id': device_id}
        self.dictionary['phase offset'] = payload[3]<<8 | payload[2]
        self.dictionary['dc offset'] = payload[5]<<8 | payload[4]
        self.dictionary['valid'] = payload[6]
        self.dictionary['data'] = {}
        firstGainIdx = -1
        if payload[7] & 1 > 0:
            for i in range(7):
                if payload[7] & (0x1<<(i+1)) > 0:
                    firstGainIdx = i
                    break
        if firstGainIdx >= 0:
            for i in range(firstGainIdx, 7):
                if payload[7] & (0x1<<(i+1)) > 0:
                    self.dictionary['data'][i] = [\
                        # current fit data, numerator, denumerator, offset
                        unpack(payload[8+(i-firstGainIdx)*26:8+(i-firstGainIdx)*26+4]),
                        unpack(payload[8+(i-firstGainIdx)*26+4:8+(i-firstGainIdx)*26+8]),
                        convertSign(unpack(payload[8+(i-firstGainIdx)*26+8:8+(i-firstGainIdx)*26+12])),
                        # power fit data, numerator, denumerator, offset
                        unpack(payload[8+(i-firstGainIdx)*26+12:8+(i-firstGainIdx)*26+16]),
                        unpack(payload[8+(i-firstGainIdx)*26+16:8+(i-firstGainIdx)*26+20]),
                        convertSign(unpack(payload[8+(i-firstGainIdx)*26+20:8+(i-firstGainIdx)*26+24])),
                        # dc offset
                        payload[8+(i-firstGainIdx)*26+24] + (payload[8+(i-firstGainIdx)*26+25]<<8)]

        
