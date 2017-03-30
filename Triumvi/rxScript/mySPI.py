
import mraa
class mySPI(object):
    def __init__(self, cs, spi_mode=mraa.SPI_MODE3):
        self.spi = mraa.Spi(0)
        if cs==0:
            self.cs = mraa.Gpio(23)
        elif cs==1: 
            self.cs = mraa.Gpio(9)
        elif cs==2:
            self.cs = mraa.Gpio(32)
        self.cs.dir(mraa.DIR_OUT)
        self.cs.write(1)
        self.spi.frequency(2000000) # 2 MHz
        self.spi.mode(spi_mode)
        self._WRITE_MAX = 20
        # first write a dummy byte
        self.spi.writeByte(0)
    
    def setFrequency(self, freq):
        self.spi.frequency(freq)

    # 1 byte Data
    def writeByte(self, data):
        # dummy byte
        self.spi.writeByte(0)
        self.cs.write(0)
        miso = self.spi.writeByte(data)
        self.cs.write(1)
        return miso

    # byte array
    def write(self, data):
        data = bytearray(data)
        self.spi.writeByte(0)
        self.cs.write(0)
        miso = []
        for i in range(0, len(data), self._WRITE_MAX):
            miso_sub = self.spi.write(data[i:min(i+self._WRITE_MAX, len(data))])
            miso += miso_sub
        self.cs.write(1)
        return list(miso)
