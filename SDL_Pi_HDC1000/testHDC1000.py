#!/usr/bin/env python
#
# Test SDL_Pi_HDC1000
#
# January 2017
#

#imports

import sys          
import time
import datetime
import SDL_Pi_HDC1000



# Main Program

print ""
print "Test SDL_Pi_HDC1000 Version 1.0 - SwitchDoc Labs" 
print ""
print "Sample uses 0x40 and SwitchDoc HDC1000 Breakout board "
print "Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S")
print ""

hdc1000 = SDL_Pi_HDC1000.SDL_Pi_HDC1000()

print "------------"
print "Manfacturer ID=0x%X"% hdc1000.readManufacturerID()  
print "Device ID=0x%X"% hdc1000.readDeviceID()  
print "Serial Number ID=0x%X"% hdc1000.readSerialNumber()  
while True:
    
        print "-----------------"
        print "Temperature = %3.1f C" % hdc1000.readTemperature()
        print "Humidity = %3.1f %%" % hdc1000.readHumidity()

        # read configuration register
        print "configure register = 0x%X" % hdc1000.readConfigRegister()
        # turn heater on
        print "turning Heater On" 
        hdc1000.turnHeaterOn() 
        # read configuration register
        print "configure register = 0x%X" % hdc1000.readConfigRegister()
        # turn heater off
        print "turning Heater Off"
        hdc1000.turnHeaterOff() 
        # read configuration register
        print "configure register = 0x%X" % hdc1000.readConfigRegister()

        # change temperature resolution
        print "change temperature resolution"
        hdc1000.setTemperatureResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_TEMPERATURE_RESOLUTION_11BIT)
        # read configuration register
        print "configure register = 0x%X" % hdc1000.readConfigRegister()
        # change temperature resolution
        print "change temperature resolution"
        hdc1000.setTemperatureResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_TEMPERATURE_RESOLUTION_14BIT)
        # read configuration register
        print "configure register = 0x%X" % hdc1000.readConfigRegister()

        # change humdity resolution
        print "change humidity resolution"
        hdc1000.setHumidityResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_HUMIDITY_RESOLUTION_8BIT)
        # read configuration register
        print "configure register = 0x%X" % hdc1000.readConfigRegister()
        # change humdity resolution
        print "change humidity resolution"
        hdc1000.setHumidityResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_HUMIDITY_RESOLUTION_14BIT)
        # read configuration register
        print "configure register = 0x%X" % hdc1000.readConfigRegister()

        time.sleep(3.0)
