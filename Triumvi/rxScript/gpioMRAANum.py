
CONVERT_TABLE = 'gpioMRAANum.txt'

class gpio_mraa(object):
    def __init__(self):
        self.gpioToMRAA = {}
        self.MRAAToGpio = {}
        with open(CONVERT_TABLE) as fp: data = fp.readlines()[1:]
        fp.close()
        data = [i.split() for i in data]
        for d in data:
            mraaNum, gpioNum = int(d[0]), int(d[1][2:])
            self.MRAAToGpio[mraaNum] = gpioNum
            self.gpioToMRAA[gpioNum] = mraaNum


