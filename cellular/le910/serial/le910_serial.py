
import serial
import time
import threading

SERIALPORT = '/dev/ttyUSB3'
BAUDRATE = 115200

class le910_serial(object):
    def __init__(self):
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
        self._command_sets = {  'at':'AT\r\n', \
                                'start_location_service':'AT$GPSSLSR=2,3,,,,,1\r\n', \
                                'stop_location_service':'AT$GPSSTOP=1\r\n', \
                                'unsolicited_nmea_data':'AT$GPSNMUN=3,1,0,0,0,0,0\r\n', \
                                'stop_unsolicited_nmea_data':'+++'} # no new line for this command

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

    def write(self, cmd):
        cmd = cmd.lower()
        at_code = self._command_sets.get(cmd, None)
        if at_code:
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
        

