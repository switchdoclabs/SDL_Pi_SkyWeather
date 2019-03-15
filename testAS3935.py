#!/usr/bin/env python
import sys

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


	# turn I2CBus 1 on
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

sensor.set_indoors(True)
sensor.set_noise_floor(0)
sensor.calibrate(tun_cap=0x0F)


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

print "Waiting for lightning - or at least something that looks like it"

while True:
    time.sleep(1.0)
