class waveformPacketFormatter(object):
    def __init__(self, packet0, packet1):
        self.wdict = {}
        if packet0.dictionary['payload'][2] == packet1.dictionary['payload'][2] and \
            abs(packet0.dictionary['payload'][3] - packet1.dictionary['payload'][3])==1:
            
            self.wdict['valid'] = True
            self.wdict['ID'] = (packet0.dictionary['payload'][2]*256 + packet0.dictionary['payload'][3])/2
            self.wdict['Current Gain'] = packet0.dictionary['payload'][4]
            self.wdict['INA Gain'] = packet0.dictionary['payload'][5]
            self.wdict['DC offset'] = packet0.dictionary['payload'][6]*256 + packet0.dictionary['payload'][7]
            # order reversed, switch them back
            if packet0.dictionary['payload'][3] > packet1.dictionary['payload'][3]:
                packet0, packet1 = packet1, packet0

            self.wdict['Waveform'] = current_waveform = self.extract_data(packet0) + self.extract_data(packet1)
                
            ##def current_transform(value):
            ##    return float((value - self.dc_offset)*self.I_transform)/self.ina_gain

            ##self.waveform = map(current_transform, current_waveform)

        else:
            self.wdict['valid'] = False


    def extract_data(self, packet):
        res = []
        def recombineData(data):
            if len(data) == 3:
                return [(data[0]<<4) + ((data[1]&240)>>4), ((data[1]&15)<<8) + (data[2])]
            else:
                return [0, 0]

        for i in range(packet.dictionary['payload'][8]/2):
            [v0, v1] = recombineData(packet.dictionary['payload'][9+3*i:9+3*(i+1)])
            res.append(v0)
            res.append(v1)
        return res
        
