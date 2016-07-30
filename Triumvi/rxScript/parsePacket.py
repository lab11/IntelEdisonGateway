
class packet(object):
    def __init__(self, data):
        self.dictionary = {}
        self.dictionary['FCF'] = data[:2]
        self.dictionary['sequence_number'] = data[2]
        # frame types
        # 0 --> Beacon
        # 1 --> Data
        # 2 --> ACK
        # 3 --> MAC command
        # 4~7 --> Reserved
        self.dictionary['frame_type'] = data[0] & 3
        self.dictionary['security_enable'] = True if (data[0] & 8)>0 else False
        self.dictionary['frame_pending'] = True if (data[0] & 16)>0 else False
        self.dictionary['ack_request'] = True if (data[0] & 32)>0 else False
        self.dictionary['PAN_ID_compression'] = True if (data[0] & 64)>0 else False
        self.dictionary['dest_addr_mode'] = (data[1] & 12)>>2
        self.dictionary['frame_version'] = (data[1] & 48)>>4
        self.dictionary['src_addr_mode'] = (data[1] & 192)>>6

        if self.dictionary['dest_addr_mode'] == 0:
            dest_PAN_ID_len = 0
            dest_addr_len = 0
        elif self.dictionary['dest_addr_mode'] == 2:
            dest_PAN_ID_len = 2
            dest_addr_len = 2
        elif self.dictionary['dest_addr_mode'] == 3:
            dest_PAN_ID_len = 2
            dest_addr_len = 8
        
        if self.dictionary['src_addr_mode'] == 0:
            src_PAN_ID_len = 0
            src_addr_len = 0
        elif self.dictionary['src_addr_mode'] == 2:
            src_PAN_ID_len = 2
            src_addr_len = 2
        elif self.dictionary['src_addr_mode'] == 3:
            src_PAN_ID_len = 2
            src_addr_len = 8
        
        if dest_PAN_ID_len > 0:
            self.dictionary['dest_PAN_ID'] = data[3:5][::-1]
            self.dictionary['dest_address'] = data[5:5+dest_addr_len][::-1]
            if self.dictionary['PAN_ID_compression']:
                src_PAN_ID_len = 0
                self.dictionary['src_PAN_ID'] = data[3:5][::-1]

        if src_PAN_ID_len > 0:
            self.dictionary['src_PAN_ID'] = data[3+dest_PAN_ID_len+dest_addr_len:3+dest_PAN_ID_len+dest_addr_len+2][::-1]
        if src_addr_len > 0:
            self.dictionary['src_address'] = data[3+dest_PAN_ID_len+dest_addr_len+src_PAN_ID_len:3+dest_PAN_ID_len+dest_addr_len+src_PAN_ID_len+src_addr_len][::-1]
        self.dictionary['payload'] = data[3+dest_PAN_ID_len+dest_addr_len+src_PAN_ID_len+src_addr_len:]
        
