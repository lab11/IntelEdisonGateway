
import socket
import signal
import sys

HOST = '141.212.11.247'
PORT = 4910

def main():
    skt = socket.socket()
    skt.bind((HOST, PORT))

    def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        skt.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        skt.listen(1)
        c, addr = skt.accept()
        print('connection from: {0}'.format(addr))
        while True:
            data = c.recv(1024)
            print(data)
            if not data:
                break

if __name__=="__main__":
    main():
