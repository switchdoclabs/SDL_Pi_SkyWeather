#!/usr/bin/env python
import sys

# Check for user imports
try:
            import conflocal as config
except ImportError:
            import config


sys.path.append('./SDL_Pi_TCA9545')
sys.path.append('./RaspberryPi-AS3935/RPi_AS3935')


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


	# turn I2CBus 1 on to reduce loading on I2CBus 0
	tca9545.write_control_register(TCA9545_CONFIG_BUS1)
	TCA9545_I2CMux_Present = True
except:
	print ">>>>>>>>>>>>>>>>>>><<<<<<<<<<<"
	print "TCA9545 I2C Mux Not Present" 
	print ">>>>>>>>>>>>>>>>>>><<<<<<<<<<<"
	TCA9545_I2CMux_Present = False

from RPi_AS3935 import RPi_AS3935

import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)

# Rev. 1 Raspberry Pis should leave bus set at 0, while rev. 2 Pis should set
# bus equal to 1. The address should be changed to match the address of the
# sensor. (Common implementations are in README.md)
sensor = RPi_AS3935(address=0x02, bus=1)

#set values for lightning
# format: [NoiseFloor, Indoor, TuneCap, DisturberDetection, WatchDogThreshold, SpikeDetection]
# default: [2,1,7,0,3,3]
NoiseFloor = config.AS3935_Lightning_Config[0]
Indoor = config.AS3935_Lightning_Config[1]
TuneCap = config.AS3935_Lightning_Config[2]
DisturberDetection = config.AS3935_Lightning_Config[3]
WatchDogThreshold = config.AS3935_Lightning_Config[4]
SpikeDetection = config.AS3935_Lightning_Config[5]



try:
    sensor.set_noise_floor(NoiseFloor)
    sensor.set_indoors(Indoor)
    sensor.calibrate(tun_cap=TuneCap)
    sensor.set_mask_disturber(DisturberDetection)
    sensor.set_watchdog_threshold(WatchDogThreshold)
    sensor.set_spike_detection(SpikeDetection)
except:
    print "AS3935 NOT detected at I2C port 0x02 on base Bus"
    exit()


def handle_interrupt(channel):
    time.sleep(0.003)
    global sensor
    reason = sensor.get_interrupt()
    if reason == 0x01:
        print "Noise level too high - adjusting"
        sensor.raise_noise_floor()
    elif reason == 0x04:
        print "Disturber detected - masking"
        sensor.set_mask_disturber(True)
    elif reason == 0x08:
        now = datetime.now().strftime('%H:%M:%S - %Y/%m/%d')
        distance = sensor.get_distance()
        print "We sensed lightning!"
        print "It was " + str(distance) + "km away. (%s)" % now
        print ""

pin = 16

#GPIO.setup(pin, GPIO.IN )
GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP )
GPIO.add_event_detect(pin, GPIO.RISING, callback=handle_interrupt)

print "AS3935 detected at I2C port 0x02"
print "Waiting for lightning - or at least something that looks like it"

while True:
    time.sleep(1.0)
