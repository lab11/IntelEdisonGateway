
import current_sink
import sys

def main():
    # this polyfit coefficient is generated from simulation with 4.99 sense resistor
    fit_coefficients = [ 0.00028722, -0.0086579,   0.18168153,  0.1596376 ]
    my_sink = current_sink.current_sink(fit_coefficients)
    
    my_sink.set_current(0, float(sys.argv[1])) # channel, mA

if __name__=="__main__":
    main()
