
import time
import le910_serial
import signal
import sys

def main():
    try:
        le910 = le910_serial.le910_serial()
    except:
        exit()

    def signal_handler(signal, frame):
        print('Exiting program...')
        le910.stop()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    le910.write('AT')
    time.sleep(1)
    le910.write('start_location_service')
    time.sleep(1)
    le910.write('unsolicited_nmea_data')

    cnt = 10

    while cnt > 0:
        if le910.data_available():
            print('Data: {:}'.format(le910.get_data().rstrip()))
            cnt -= 1
        else:
            time.sleep(1)
    le910.write('stop_unsolicited_nmea_data')
    time.sleep(1)
    le910.write('stop_location_service')
    time.sleep(1)
    print(le910.read_buf)
    le910.stop()
        
if __name__=='__main__':
    main()
