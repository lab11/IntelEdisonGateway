

import socket
import sys
import signal

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 4909

DEST_HOST = 'lab11power.ddns.net'
DEST_PORT = 4908

WARNING_HOST = '141.212.11.247'
WARNING_PORT = 4910

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

    warn_skt = socket.socket()
    try:
        warn_skt.connect((WARNING_HOST, WARNING_PORT))
    except:
        print('cannot connect to waring server')
        raise

    def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

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

            print("Command Received")
            if cmd[1] == APS3B12_ENABLE:
                if cmd[2] == 1 and mydevice.state == 'off':
                    print("Turn on the load")
                    dest_skt.send('on')
                    mydevice.state = 'on'
                elif cmd[2] == 0 and mydevice.state == 'on':
                    print("Turn off the load")
                    dest_skt.send('off')
                    mydevice.state = 'off'
            elif cmd[1] == APS3B12_SET_CURRENT and mydevice.state == 'on':
                currentVal = float(int(cmd[2])*256 + int(cmd[3]))/1000
                if mydevice.currentVal != currentVal and currentVal <= MAX_CURRENT_AVAIABLE:
                    print("Set load current to: {:}".format(currentVal))
                    if currentVal - mydevice.currentVal > 0.25:
                        warn_skt.send('Warning, inconsistent increase')
                    dest_skt.send('amp='+str(currentVal))
                    mydevice.currentVal = currentVal

    local_skt.close()
    dest_skt.close()
    warn_skt.close()

if __name__=='__main__':
    main()
