#!/usr/bin/env python
#
# SDL_Pi_WeatherRack Example Test File 
# Version 1.0 February 12, 2015
#
# SwitchDoc Labs
# www.switchdoc.com
#
#


#imports

import time
import sys

sys.path.append('SDL_Adafruit_ADS1x15')
sys.path.append('SDL_Pi_WeatherRack')

import config

import SDL_Pi_WeatherRack as SDL_Pi_WeatherRack

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

            
# GPIO Numbering Mode GPIO.BCM
#

# constants


#sample mode means return immediately.  THe wind speed is averaged at sampleTime or when you ask, whichever is longer
SDL_MODE_SAMPLE = 0
#Delay mode means to wait for sampleTime and the average after that time.
SDL_MODE_DELAY = 1

anenometerPin = 20
rainPin = 13
#anenometerPin = 6
#rainPin = 12

# constants

SDL_MODE_INTERNAL_AD = 0
SDL_MODE_I2C_ADS1015 = 1    # internally, the library checks for ADS1115 or ADS1015 if found

#sample mode means return immediately.  THe wind speed is averaged at sampleTime or when you ask, whichever is longer
SDL_MODE_SAMPLE = 0
#Delay mode means to wait for sampleTime and the average after that time.
SDL_MODE_DELAY = 1

weatherStation = SDL_Pi_WeatherRack.SDL_Pi_WeatherRack(anenometerPin, rainPin, 0,0, SDL_MODE_I2C_ADS1015)

weatherStation.setWindMode(SDL_MODE_SAMPLE, 5.0)
#weatherStation.setWindMode(SDL_MODE_DELAY, 5.0)

maxEverWind = 0.0
maxEverGust = 0.0
totalRain = 0
while True:


 	print "---------------------------------------- "
        print "----------------- "
        print " SDL_Pi_WeatherRack Library"
        print " WeatherRack Weather Sensors"
        print "----------------- "
        #

        currentWindSpeed = weatherStation.current_wind_speed()/1.609
        currentWindGust = weatherStation.get_wind_gust()/1.609
        totalRain = totalRain + (weatherStation.get_current_rain_total()/25.4)
        print("Rain Total=\t%0.2f in")%(totalRain)
        print("Wind Speed=\t%0.2f MPH")%(currentWindSpeed)
	if currentWindSpeed > maxEverWind:
		maxEverWind = currentWindSpeed

	if currentWindGust > maxEverGust:
		maxEverGust = currentWindGust

        print("max Ever Wind Speed=\t%0.2f MPH")%(maxEverWind)
        print("MPH wind_gust=\t%0.2f MPH")%(currentWindGust)
        print("max Ever Gust wind_gust=\t%0.2f MPH")%(maxEverGust)
        print "Wind Direction=\t\t\t %0.2f Degrees" % weatherStation.current_wind_direction()

        print "Wind Direction Voltage=\t\t %0.3f V" % weatherStation.current_wind_direction_voltage()

        print "----------------- "
        print "----------------- "

	time.sleep(5.0)
