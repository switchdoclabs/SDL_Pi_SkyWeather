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


        # turn I2CBus 0 on
        tca9545.write_control_register(TCA9545_CONFIG_BUS0)
        TCA9545_I2CMux_Present = True
except:
        print ">>>>>>>>>>>>>>>>>>><<<<<<<<<<<"
        print "TCA9545 I2C Mux Not Present" 
        print ">>>>>>>>>>>>>>>>>>><<<<<<<<<<<"
sys.path.append('./SDL_Pi_AM2315')

import AM2315

am2315 = AM2315.AM2315(powerpin=6)

for x in range(0,10):
    outsideHumidity, outsideTemperature, crc_check = am2315.read_humidity_temperature_crc() 
    print "temperature: %0.1f" % outsideTemperature
    print "humidity: %0.1f" % outsideHumidity
    print "crc: %s" % crc_check
    print
    time.sleep(2.0)
