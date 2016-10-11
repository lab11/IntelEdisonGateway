
from mySPI import mySPI
from edisonLED import edisonLED
from time import sleep
import mraa
from parsePacket import *
from triumviDecrypt import triumviDecrypt
from triumviPacketFormatter import *

import threading

CC2538INTPINNUM = 38 # MRAA number, GP43
CC2538RESETPINNUM = 51 # MRAA number, GP41
MAX_TRIUMVI_PKT_LEN = 50 # maximum triumvi packet length
MIN_TRIUMVI_PKT_LEN = 14 # minimum triumvi packet length
MAX_FLUSH_THRESHOLD = 32 # maximum trials before reset cc2538
TRIUMVI_PACKET_ID = 160 # triumvi packet ID

# Controlling APS3B12 
import socket
HOST = '127.0.0.1'
PORT = 4909
APS3B12_PACKET_ID = 31 # APS control packet ID
# end of controlling APS3B12

KEY = ['0x46', '0xe2', '0xe5', '0x28', '0x9a', '0x65', '0x3c', '0xe9', '0x0', '0x2f', '0xc1', '0x6e', '0x65', '0xee', '0xc', '0x3e']

condition = threading.Condition()

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

        condition.acquire()
        while True:
            condition.wait()
            # When we have been notified we want to read the cc2538
            self.cc2538ISR()

            # Keep reading while there are pending interrupts
            while self.cc2538DataReadyInt.read() == 1:
                self.cc2538ISR()

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
        if newPacket and newPacket.dictionary['payload'][0] == TRIUMVI_PACKET_ID:
            decrypted_data = triumviDecrypt(KEY, newPacket.dictionary['src_address'], newPacket.dictionary['payload'])
            if decrypted_data:
                newPacketFormatted = triumviPacket([TRIUMVI_PACKET_ID] + newPacket.dictionary['src_address'] + decrypted_data)
                self.callback(newPacketFormatted)
                self.blueLed.leds_off()
                self.resetCount = 0
        # APS3B12 control packet
        elif newPacket and newPacket.dictionary['payload'][0] == APS3B12_PACKET_ID and len(newPacket.dictionary['payload'])==4:
            skt = socket.socket()
            try:
                skt.connect((HOST, PORT))
                myPayload = " ".join(str(x) for x in newPacket.dictionary['payload'])
                skt.send(myPayload)
                skt.close()
            except:
                pass
        # end of APS3B12 control
        elif newPacket and newPacket.dictionary['payload'][0] == 63:
            print('Calibration coefficient: {:}'.format(newPacket.dictionary['payload'][1:]))
            myFile = open('calibration_coef.txt', 'a')
            myFile.write('From: {:}'.format(newPacket.dictionary['src_address']))
            myFile.write('Data: {:}'.format(newPacket.dictionary['payload'][1:]))
            myFile.write('\r\n')
            myFile.close()

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



