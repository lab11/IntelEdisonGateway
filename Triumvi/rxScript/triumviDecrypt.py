
from Crypto.Cipher import AES

# A valid packet should look like:
# 2 Bytes Frame control field (FCF)
# 1 Byte sequence number
# Address
# payload

# This function only tries to decrypt a triumvi packet
# The valid Triumvi payload should look like:
# 1 byte ID: 0xa0
# 4 bytes counter --> last 4 bytes of nonce
# encrypted data
# 4 bytes MIC

# The 13 bytes nonce is composed of (8 bytes addr, + 0x00 + 4 bytes counter)
def triumviDecrypt(key, srcAddr, payload):

    key = ''.join([chr(int(i, 16)) for i in key])
    nonce = ''.join([chr(i) for i in srcAddr + [0] + payload[1:5]])
    adata = ''.join([chr(i) for i in srcAddr])
    pdata = ''.join(([chr(i) for i in payload[5:-4]]))
    mic = ''.join([chr(i) for i in payload[-4:]])

    cipher = AES.new(key, AES.MODE_CCM, nonce, mac_len=4)
    cipher.update(adata)

    plaintext = cipher.decrypt(pdata)
    try:
        cipher.verify(mic)
        plaintext = [ord(i) for i in plaintext]
        print('Decrypt success!')
        return plaintext
    except ValueError:
        print('Decrypt failed!')
        return None

