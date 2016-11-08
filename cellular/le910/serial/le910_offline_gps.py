
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

    print('Start location service... '),
    le910.write('start_location_service')
    print (le910.get_data_block())

    print('Set active GPS antenna...'),
    le910.write('active_gps_antenna')
    print (le910.get_data_block())

    print('Get unsolicited data... '),
    le910.write('unsolicited_nmea_data')
    print (le910.get_data_block())

    trial = 1000
    gps_data_valid = False

    while (trial > 0) and (not gps_data_valid):
        tmp = le910.get_data_block()
        print('Data received from GPS: {:}'.format(tmp)), 
        tmp = tmp.split(',')
        if len(tmp[1]) > 0:
            print ('valid data')
            gps_data_valid = True
        else:
            print ('invalid data')
        trial -= 1

    print('Stop unsolicited data...')
    le910.write('stop_unsolicited_nmea_data')
    time.sleep(3)
    le910.clear_data_buf()

    if gps_data_valid:
        le910.write('gps_acquired_position')
        gps_location = le910_serial.gps_info(le910.get_data_block())
        print(gps_location)
        

    print('Stop location service... '),
    le910.write('stop_location_service')
    print (le910.get_data_block())

    le910.stop()
        
if __name__=='__main__':
    main()
