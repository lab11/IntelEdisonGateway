
class ad5304(object):
    def __init__(self, spi_obj, resolution):
        self.spi_obj = spi_obj
        self.resolution = resolution
        self.ref_volt = 3.3

    def off(self):
        self.spi_obj.write([0x00, 0x00])

    # bits are layout as
    # A1, A0
    # PD_b
    # LDAC_b
    # D11 ~ D0
    def set_output_voltage(self, channel, voltage):
        value = max(int(round(voltage/self.ref_volt*4096)), 4095)
        # clear last 4 bit
        if self.resolution == 8:
            value &= 0xff0
        data = [((channel & 0x3)<<6) + (1<<5) + ((value & 0xf00)>>8), (value & 0xff)]
        self.spi_obj.write(data)
