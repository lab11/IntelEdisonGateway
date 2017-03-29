
import serial
import time
import threading
import datetime
import findTTY2

#SERIALPORT = '/dev/ttyUSB3'
#SERIALPORT = '/dev/tty.usbserial-AH02VOLK'
BAUDRATE = 115200

class latitude(object):
    # format should be ddmm.mmmmN/S
    def __init__(self, latitude_string):
        self.degree = int(latitude_string[0:2])
        self.minute = int(latitude_string[2:4])
        self.second = int(round(float(latitude_string[5:9])/10000*60))
        self.NS = latitude_string[-1]
    def __str__(self):
        return '{:} Degree: {:}, Minute: {:}, Second: {:}'.\
            format(self.NS, self.degree, self.minute, self.second)

class longitude(object):
    # format should be dddmm.mmmmE/W
    def __init__(self, longititude_string):
        self.degree = int(longititude_string[0:3])
        self.minute = int(longititude_string[3:5])
        self.second = int(round(float(longititude_string[6:10])/10000*60))
        self.EW = longititude_string[-1]
    def __str__(self):
        return '{:} Degree: {:}, Minute: {:}, Second: {:}'.\
            format(self.EW, self.degree, self.minute, self.second)

class gps_info(object):
    def __init__(self, gpsacp_string):
        tmp = gpsacp_string[8:].split(',')
        if len(tmp) > 1 and int(tmp[5])>1:
            self.gps_acquired = True
            self.utc_time = datetime.datetime.strptime(tmp[0][1:7], "%H%M%S").time()
            self.lat = latitude(tmp[1])
            self.lon = longitude(tmp[2])
            self.alt = float(tmp[4])
            self.speed = float(tmp[7]) # unit is km/h
            self.date = datetime.datetime.strptime(tmp[9], "%d%m%y").date()
            self.num_sat = int(tmp[10])
        else:
            self.gps_acquired = False
    def __str__(self):
        if self.gps_acquired:
            return 'Date: {:}\r\n\
                    UTC time: {:}\r\n\
                    Latitude: {:}\r\n\
                    Longitude: {:}\r\n\
                    Altitude: {:} (m)\r\n\
                    Speed: {:} (km/h)\r\n'.\
                    format(self.date, self.utc_time, self.lat, self.lon,\
                        self.alt, self.speed)
        else:
            return 'GPS location not available\r\n'

class le910_serial(object):
    def __init__(self):
        SERIALPORT = findTTY2.findSerialDevice('MINOR=\'4\'')[0]
        if not SERIALPORT:
            print('cannot find serial device')
            exit()
        self.ser = serial.Serial()
        self.ser.port = SERIALPORT
        self.ser.baudrate = BAUDRATE
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dstdts = False
        self.ser.timeout = 0.5

        try:
            self.ser.open()
            self.ser.flushInput()
            self.ser.flushOutput()
        except:
            print('cannot open device')
            exit()

        self.read_thread_event = threading.Event()
        self.read_thread = threading.Thread(target=self.read_proc, args=())
        self.read_thread.start()
        self.read_buf = []
        self.buf_lock = False
        self.last_command = None
        self._command_sets = {\
            'at'                        :'AT\r\n', \
            'shutdown'                  :'AT#shdn\r\n', \
            'start_location_service'    :'AT$GPSSLSR=2,3,,,,,1\r\n', \
            'stop_location_service'     :'AT$GPSSTOP=1\r\n', \
            'unsolicited_nmea_data'     :'AT$GPSNMUN=3,1,0,0,0,0,0\r\n', \
            'stop_unsolicited_nmea_data':'+++', \
            'gps_acquired_position'     :'AT$GPSACP\r\n', \
            'active_gps_antenna'        :'AT$GPSAT=1\r\n', \
            'get_model_name'            :'AT+GMM\r\n', \
            'get_firmware_version'      :'AT+CGMR\r\n', \
            'set_text_mode_parameter'   :'AT+CSMP="17",4098,0,2\r\n', \
            'set_message_format'        :'AT+CMGF=1\r\n', \
            'send_message'              :'AT+CMGS=', \
            'sms_body'                  :'' \
        }

    def data_available(self):
        return len(self.read_buf) != 0

    def get_data(self):
        if self.data_available():
            while self.buf_lock:
                pass
            self.buf_lock = True
            tmp = self.read_buf.pop(0)
            self.buf_lock = False
            return tmp
        else:
            return None

    def get_data_block(self):
        while not self.data_available():
            time.sleep(0.1)
        return self.get_data()

    def clear_data_buf(self):
        while self.buf_lock:
            pass
        self.buf_lock = True
        del self.read_buf[:]
        self.buf_lock = False

    def write(self, cmd, additional_arg=None):
        cmd = cmd.lower()
        at_code = self._command_sets.get(cmd, None)
        if at_code or cmd == 'sms_body':
            if additional_arg != None:
                at_code += additional_arg
            self.ser.write(at_code)
            self.last_command = at_code.rstrip()
        else:
            print('invalid command format')

    def read_proc(self):
        while not self.read_thread_event.is_set():
            tmp = self.ser.readline().rstrip()
            if tmp:
                if self.last_command and tmp == self.last_command:
                    self.last_command = None
                else:
                    while self.buf_lock:
                        pass
                    self.buf_lock = True
                    self.read_buf.append(tmp)
                    self.buf_lock = False

    def stop(self):
        self.read_thread_event.set()
        self.ser.close()
        

