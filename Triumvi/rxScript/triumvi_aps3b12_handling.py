

import socket

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 4909

DEST_HOST = 'lab11power.ddns.net'
DEST_PORT = 4908

APS3B12_PACKET_ID = 31
APS3B12_ENABLE = 1
APS3B12_SET_CURRENT = 2

MAX_CURRENT_AVAIABLE = 10 # 10 A


class aps3b12_state(object):
    def __init__(self):
        self.state = 'off'
        self.currentVal = 0


def main():
    local_skt = socket.socket()
    try:
        local_skt.bind((LOCAL_HOST, LOCAL_PORT))
    except:
        print('cannot open local port\r\n')
        raise

    dest_skt = socket.socket()
    try:
        dest_skt.connect((DEST_HOST, DEST_PORT))
    except:
        print('cannot connect to remote server\r\n')
        raise

    mydevice = aps3b12_state()

    while True:
        local_skt.listen(1)
        c, addr = local_skt.accept()
        while True:
            data = c.recv(1024).strip()
            if not data:
                break
            try:
                cmd = [int(x) for x in data.split()]
            except:
                break

            print('Command received: {:}'.format(cmd))
            if cmd[1] == APS3B12_ENABLE:
                if cmd[2] == 1:
                    dest_skt.send('on')
                    mydevice.state = 'on'
                else:
                    dest_skt.send('off')
                    mydevice.state = 'off'
            elif cmd[1] == APS3B12_SET_CURRENT:
                currentVal = float(int(cmd[2])*256 + int(cmd[3]))/1000
                if mydevice.currentVal != currentVal and currentVal <= MAX_CURRENT_AVAIABLE:
                    dest_skt.send('amp='+str(currentVal))
                    mydevice.currentVal = currentVal

    local_skt.close()
    dest_skt.close()

if __name__=='__main__':
    main()
