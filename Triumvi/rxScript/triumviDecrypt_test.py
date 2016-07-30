
from parsePacket import *
from triumviDecrypt import triumviDecrypt

KEY = ['0x46', '0xe2', '0xe5', '0x28', '0x9a', '0x65', '0x3c', '0xe9', '0x0', '0x2f', '0xc1', '0x6e', '0x65', '0xee', '0xc', '0x3e']

data = [65, 216, 98, 34, 0, 255, 255, 51, 0, 160, 82, 84, 229, 152, 192, 160, 164, 160, 119, 254, 135, 48, 140, 126, 239, 0, 58, 181, 236, 247, 157, 182, 191, 196, 189, 57, 242]

newpacket = packet(data)

if newpacket.dictionary['payload'][0] == 160:
    decrypted_data = triumviDecrypt(KEY, newpacket.dictionary['src_address'], newpacket.dictionary['payload'])
    if decrypted_data:
        print('decrypted data: {0}'.format(decrypted_data))
    
