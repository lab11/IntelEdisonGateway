
import mraa, mySPI, ad5304
class current_sink(object):
    def __init__(self, poly_fit_coefficients):
        self.spi_interface = mySPI.mySPI(2, mraa.SPI_MODE2)
        self.dac = ad5304.ad5304(self.spi_interface, 12)
        # the coefficients are the polynominal fit from current to voltage
        self.coefficients = poly_fit_coefficients

    def set_current(self, channel, current):
        max_power = len(self.coefficients)-1
        result = 0
        for i in range(len(self.coefficients)):
            result += self.coefficients[i]*(float(current)**(max_power-i))
        self.dac.set_output_voltage(channel, result)

            
