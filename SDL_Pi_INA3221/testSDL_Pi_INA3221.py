#!/usr/bin/env python
#
# Test SDL_Pi_INA3221
# John C. Shovic, SwitchDoc Labs
# 03/05/2015
#
#

# imports

import sys
import time
import datetime
import random 
import SDL_Pi_INA3221

# Main Program

print ""
print "Test SDL_Pi_INA3221 Version 1.0 - SwitchDoc Labs"
print ""
print "Sample uses 0x40 and SunAirPlus board INA3221"
print " Will work with the INA3221 SwitchDoc Labs Breakout Board"
print "Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S")
print ""

filename = time.strftime("%Y-%m-%d%H:%M:%SRTCTest") + ".txt"
starttime = datetime.datetime.utcnow()

ina3221 = SDL_Pi_INA3221.SDL_Pi_INA3221(addr=0x40)

# the three channels of the INA3221 named for SunAirPlus Solar Power Controller channels (www.switchdoc.com)
LIPO_BATTERY_CHANNEL = 1
SOLAR_CELL_CHANNEL   = 2
OUTPUT_CHANNEL       = 3


while True:

  	print "------------------------------"
  	shuntvoltage1 = 0
  	busvoltage1   = 0
  	current_mA1   = 0
  	loadvoltage1  = 0


  	busvoltage1 = ina3221.getBusVoltage_V(LIPO_BATTERY_CHANNEL)
  	shuntvoltage1 = ina3221.getShuntVoltage_mV(LIPO_BATTERY_CHANNEL)
  	# minus is to get the "sense" right.   - means the battery is charging, + that it is discharging
  	current_mA1 = ina3221.getCurrent_mA(LIPO_BATTERY_CHANNEL)  

  	loadvoltage1 = busvoltage1 + (shuntvoltage1 / 1000)
  
  	print "LIPO_Battery Bus Voltage: %3.2f V " % busvoltage1
  	print "LIPO_Battery Shunt Voltage: %3.2f mV " % shuntvoltage1
  	print "LIPO_Battery Load Voltage:  %3.2f V" % loadvoltage1
  	print "LIPO_Battery Current 1:  %3.2f mA" % current_mA1
  	print

  	shuntvoltage2 = 0
  	busvoltage2 = 0
  	current_mA2 = 0
  	loadvoltage2 = 0

  	busvoltage2 = ina3221.getBusVoltage_V(SOLAR_CELL_CHANNEL)
  	shuntvoltage2 = ina3221.getShuntVoltage_mV(SOLAR_CELL_CHANNEL)
  	current_mA2 = -ina3221.getCurrent_mA(SOLAR_CELL_CHANNEL)
  	loadvoltage2 = busvoltage2 + (shuntvoltage2 / 1000)
  
  	print "Solar Cell Bus Voltage 2:  %3.2f V " % busvoltage2
  	print "Solar Cell Shunt Voltage 2: %3.2f mV " % shuntvoltage2
  	print "Solar Cell Load Voltage 2:  %3.2f V" % loadvoltage2
  	print "Solar Cell Current 2:  %3.2f mA" % current_mA2
  	print 

  	shuntvoltage3 = 0
  	busvoltage3 = 0
  	current_mA3 = 0
  	loadvoltage3 = 0

  	busvoltage3 = ina3221.getBusVoltage_V(OUTPUT_CHANNEL)
  	shuntvoltage3 = ina3221.getShuntVoltage_mV(OUTPUT_CHANNEL)
  	current_mA3 = ina3221.getCurrent_mA(OUTPUT_CHANNEL)
  	loadvoltage3 = busvoltage3 + (shuntvoltage3 / 1000)
  
  	print "Output Bus Voltage 3:  %3.2f V " % busvoltage3
  	print "Output Shunt Voltage 3: %3.2f mV " % shuntvoltage3
  	print "Output Load Voltage 3:  %3.2f V" % loadvoltage3
  	print "Output Current 3:  %3.2f mA" % current_mA3
  	print
		

	#
	time.sleep(2.0)
