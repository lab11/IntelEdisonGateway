
import sys
import mraa, mySPI, ad5304
import time

def main():
    spi = mySPI.mySPI(2, mraa.SPI_MODE2)
    time.sleep(0.5)
    dac = ad5304.ad5304(spi, 12)
    # channel, value
    dac.set_output_voltage(int(sys.argv[1]), float(sys.argv[2]))
    
if __name__=="__main__":
    main()
