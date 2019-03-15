import sys
sys.path.append('./TSL2591')


import TSL2591 

tsl = TSL2591.Tsl2591()  # initialize
full, ir = tsl.get_full_luminosity()  # read raw values (full spectrum and ir spectrum)
lux = tsl.calculate_lux(full, ir)  # convert raw values to lux
print (lux, full, ir)
print ()

def test(int_time=TSL2591.INTEGRATIONTIME_100MS, gain=TSL2591.GAIN_LOW):
        tsl.set_gain(gain)
        tsl.set_timing(int_time)
        full_test, ir_test = tsl.get_full_luminosity()
        lux_test = tsl.calculate_lux(full_test, ir_test)
        print ('Lux = %f  full = %i  ir = %i' % (lux_test, full_test, ir_test))
        print("integration time = %i" % tsl.get_timing())
        print("gain = %i \n" % tsl.get_gain())        

for i in [TSL2591.INTEGRATIONTIME_100MS,
              TSL2591.INTEGRATIONTIME_200MS,
              TSL2591.INTEGRATIONTIME_300MS,
              TSL2591.INTEGRATIONTIME_400MS,
              TSL2591.INTEGRATIONTIME_500MS,
              TSL2591.INTEGRATIONTIME_600MS]:
        test(i, TSL2591.GAIN_LOW)

for i in [TSL2591.GAIN_LOW,
              TSL2591.GAIN_MED,
              TSL2591.GAIN_HIGH,
              TSL2591.GAIN_MAX]:
        test(TSL2591.INTEGRATIONTIME_100MS, i)
