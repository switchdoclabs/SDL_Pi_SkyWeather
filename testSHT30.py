#!/usr/bin/env python
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


sys.path.append('./SDL_Pi_SHT30')

import SHT30
thsen = SHT30.SHT30(powerpin=6)

while (1):
	print "T   ", thsen.read_temperature()
	print "H   ", thsen.read_humidity()
	print "H,T ", thsen.read_humidity_temperature()
	print "H,T,C ", thsen.read_humidity_temperature_crc()
        h,t,cH,cT = thsen.read_humidity_temperature_crc()
        print "CRCH=0x%02x" % cH
        print "CRCT=0x%02x" % cT

