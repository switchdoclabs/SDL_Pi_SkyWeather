import sys
sys.path.append('./TSL2591')


import time
import sys
sys.path.append('./SDL_Pi_TCA9545')

import SDL_Pi_TCA9545




################
# TCA9545 I2C Mux 

#/*=========================================================================
#    I2C ADDRESS/BITS
#    -----------------------------------------------------------------------*/
TCA9545_ADDRESS =                         (0x73)    # 1110011 (A0+A1=VDD)
#/*=========================================================================*/

#/*=========================================================================
#    CONFIG REGISTER (R/W)
#    -----------------------------------------------------------------------*/
TCA9545_REG_CONFIG            =          (0x00)
#    /*---------------------------------------------------------------------*/

TCA9545_CONFIG_BUS0  =                (0x01)  # 1 = enable, 0 = disable 
TCA9545_CONFIG_BUS1  =                (0x02)  # 1 = enable, 0 = disable 
TCA9545_CONFIG_BUS2  =                (0x04)  # 1 = enable, 0 = disable 
TCA9545_CONFIG_BUS3  =                (0x08)  # 1 = enable, 0 = disable 

#/*=========================================================================*/

# I2C Mux TCA9545 Detection
try:
        tca9545 = SDL_Pi_TCA9545.SDL_Pi_TCA9545(addr=TCA9545_ADDRESS, bus_enable = TCA9545_CONFIG_BUS0)


        # turn I2CBus 3 on
        tca9545.write_control_register(TCA9545_CONFIG_BUS3)
        TCA9545_I2CMux_Present = True
except:
        print ">>>>>>>>>>>>>>>>>>><<<<<<<<<<<"
        print "TCA9545 I2C Mux Not Present" 
        print ">>>>>>>>>>>>>>>>>>><<<<<<<<<<<"

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
