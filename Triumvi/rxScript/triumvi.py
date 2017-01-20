
from mySPI import mySPI
from edisonLED import edisonLED
import time
import mraa
from parsePacket import *
from triumviDecrypt import triumviDecrypt
from triumviPacketFormatter import *
import signal
import sys

import threading

CC2538INTPINNUM = 38 # MRAA number, GP43
CC2538RESETPINNUM = 51 # MRAA number, GP41
MAX_TRIUMVI_PKT_LEN = 50 # maximum triumvi packet length
MIN_TRIUMVI_PKT_LEN = 14 # minimum triumvi packet length
MAX_FLUSH_THRESHOLD = 32 # maximum trials before reset cc2538
TRIUMVI_PACKET_ID = 160 # triumvi packet ID
# Controlling APS3B12 
import socket
HOST = 'lab11power.ddns.net'
PORT = 4908
APS3B12_PACKET_ID = 31 # APS control packet ID
APS3B12_ENABLE = 1
APS3B12_SET_CURRENT = 2
APS3B12_READ_CURRENT = 0
APS3B12_READ = 3
APS3B12_CURRENT_INFO = 3
# end of controlling APS3B12
# RTC related
TRIUMVI_RTC = 172
TRIUMVI_RTC_SET = 255
TRIUMVI_RTC_REQ = 254

# initial current setting while calibrating triumvi
CALIBRATION_START_SETTING = 0.75


KEY = ['0x46', '0xe2', '0xe5', '0x28', '0x9a', '0x65', '0x3c', '0xe9', '0x0', '0x2f', '0xc1', '0x6e', '0x65', '0xee', '0xc', '0x3e']

condition = threading.Condition()

class aps3b12_state(object):
    def __init__(self):
        self.state = 'off'
        self.currentVal = 0.0

myDevice = aps3b12_state()


def triumviCallBackISR(args):
    # args.cc2538ISR()
    condition.acquire()
    condition.notify()
    condition.release()

class triumvi(object):
    def __init__(self, callback):
        self.callback = callback
        self.cc2538Spi = mySPI(0)
        self.cc2520Spi = mySPI(1)
        self.cc2538DataReadyInt = mraa.Gpio(CC2538INTPINNUM)
        self.cc2538DataReadyInt.dir(mraa.DIR_IN)
        self.cc2538DataReadyInt.isr(mraa.EDGE_RISING, triumviCallBackISR, 8)
        self.cc2538Reset = mraa.Gpio(CC2538RESETPINNUM)
        self.cc2538Reset.dir(mraa.DIR_OUT)
        self.cc2538Reset.write(0) # active low
        self.cc2538Reset.write(1) # active low
        self.resetCount = 0

        self.redLed     = edisonLED('red')
        self.greenLed   = edisonLED('green')
        self.blueLed    = edisonLED('blue')
        # macro, don't touch
        self._SPI_MASTER_REQ_DATA = 0
        self._SPI_MASTER_DUMMY = 1
        self._SPI_MASTER_GET_DATA = 2
        self._SPI_MASTER_RADIO_ON = 3
        self._SPI_MASTER_RADIO_OFF = 4
        self._SPI_RF_PACKET_SEND = 5
        self._SPI_MASTER_SET_TIME = 6
        # delay 0.5 seconds for 2538 to boot
        time.sleep(0.5)
        self.updateTimeThreadEvent = threading.Event()
        self.updateTimeThread = threading.Thread(target=self.updateTime, args=())
        self.updateTimeThread.start()

        signal.signal(signal.SIGINT, self.signal_handler)

        condition.acquire()
        while not self.updateTimeThreadEvent.is_set():
            condition.wait()
            # When we have been notified we want to read the cc2538
            self.cc2538ISR()

            # Keep reading while there are pending interrupts
            while self.cc2538DataReadyInt.read() == 1:
                self.cc2538ISR()

    def updateTime(self):
        # get local time every 30 seconds
        while not self.updateTimeThreadEvent.is_set():
            UTC_TIME = time.gmtime()
            dataout = [self._SPI_MASTER_SET_TIME, 7]+[UTC_TIME.tm_year-2000, UTC_TIME.tm_mon, UTC_TIME.tm_mday, UTC_TIME.tm_hour, UTC_TIME.tm_min, UTC_TIME.tm_sec]
            dummy = self.cc2538Spi.write(dataout)
            time.sleep(30)

    def requestData(self):
        dummy = self.cc2538Spi.writeByte(self._SPI_MASTER_REQ_DATA)

    def getData(self):
        length = self.cc2538Spi.writeByte(self._SPI_MASTER_DUMMY)
        if length < MIN_TRIUMVI_PKT_LEN or length > MAX_TRIUMVI_PKT_LEN:
            self.flushCC2538TXFIFO()
            return
        self.blueLed.leds_on()
        #print('data length: {0}'.format(length))
        dataOut = [self._SPI_MASTER_GET_DATA, length-1] + (length-2)*[0]
        data = self.cc2538Spi.write(dataOut)
        #print("Data: {0}".format(data))
        timeStamp = datetime.now()
        # print('Time Stamp: {0}, {1:02d}/{2:02d}, {3:02d}:{4:02d}:{5:02d}'.\
        #     format(timeStamp.year, timeStamp.month, timeStamp.day,\
        #     timeStamp.hour, timeStamp.minute, timeStamp.second))
        #newPacket = triumviPacket(data)
        #if newPacket:
        #    self.callback(newPacket)
        #    self.blueLed.leds_off()
        #    self.resetCount = 0
        newPacket = packet(data)
        if newPacket and 'payload' in newPacket.dictionary and newPacket.dictionary['payload'][0] == TRIUMVI_PACKET_ID:
            decrypted_data = triumviDecrypt(KEY, newPacket.dictionary['src_address'], newPacket.dictionary['payload'])
            if decrypted_data:
                newPacketFormatted = triumviPacket([TRIUMVI_PACKET_ID] + newPacket.dictionary['src_address'] + decrypted_data)
                self.callback(newPacketFormatted)
                self.resetCount = 0
        # APS3B12 control packet
        elif newPacket and 'payload' in newPacket.dictionary and newPacket.dictionary['payload'][0] == APS3B12_PACKET_ID and len(newPacket.dictionary['payload'])==4:
            skt = socket.socket()
            try:
                if newPacket.dictionary['payload'][1] == APS3B12_ENABLE:
                    if myDevice.state == 'off' and newPacket.dictionary['payload'][2] == 1:
                        skt.connect((HOST, PORT))
                        skt.send('on')
                        myDevice.state = 'on'
                    elif myDevice.state == 'on' and newPacket.dictionary['payload'][2] == 0:
                        skt.connect((HOST, PORT))
                        skt.send('off')
                        myDevice.state = 'off'
                elif newPacket.dictionary['payload'][1] == APS3B12_SET_CURRENT:
                    currentVal = float(int(newPacket.dictionary['payload'][2])*256 + int(newPacket.dictionary['payload'][3]))/1000
                    if currentVal > myDevice.currentVal or (currentVal < (myDevice.currentVal - 1.5)) or (currentVal == CALIBRATION_START_SETTING and abs(currentVal - myDevice.currentVal) > 0.01):
                        print("Set load current to: {:}".format(currentVal))
                        skt.connect((HOST, PORT))
                        skt.send('amp='+str(currentVal))
                        myDevice.currentVal = currentVal
                        print("Flushing FIFO...")
                        self.flushCC2538TXFIFO()
                elif newPacket.dictionary['payload'][1] == APS3B12_READ:
                    if newPacket.dictionary['payload'][2] == APS3B12_READ_CURRENT:
                        skt.connect((HOST, PORT))
                        skt.send('readI')
                        value = skt.recv(1024).strip()
                        try:
                            value = float(value)
                        except:
                            value = None
                        if value:
                            print('Read Current: {:}'.format(value))
                            myDevice.currentVal = value
                            value = int(value*1000)
                            value_arr = []
                            for i in range(4):
                                value_arr.append(value%256)
                                value /= 256
                            dataout = [self._SPI_RF_PACKET_SEND, 7, APS3B12_PACKET_ID, APS3B12_CURRENT_INFO]+value_arr[::-1]
                            dummy = self.cc2538Spi.write(dataout)
                skt.close()
            except:
                pass
        self.blueLed.leds_off()
            

    def flushCC2538TXFIFO(self):
        self.redLed.leds_on()
        dummy = self.cc2538Spi.write([self._SPI_MASTER_GET_DATA, MAX_TRIUMVI_PKT_LEN-1] + (MAX_TRIUMVI_PKT_LEN-2)*[0])
        self.resetCount += 1
        if self.resetCount == MAX_FLUSH_THRESHOLD:
            self.resetCount = 0
            self.resetcc2538()
        self.redLed.leds_off()

    def cc2538ISR(self):
        self.requestData()
        while self.cc2538DataReadyInt.read() == 1:
            pass
        self.getData()

    def resetcc2538(self):
        self.cc2538Reset.write(0) # active low
        self.cc2538Reset.write(1)

    def radioOn(self):
        dummy = self.cc2538Spi.writeByte(self._SPI_MASTER_RADIO_ON)

    def radioOff(self):
        dummy = self.cc2538Spi.writeByte(self._SPI_MASTER_RADIO_OFF)

    def signal_handler(self, signal, frame):
        self.updateTimeThreadEvent.set()
        sys.exit(0)

