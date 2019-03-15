
#
# calculate all graphs
#
# SwitchDoc Labs March 30, 2015

import sys
import RPi.GPIO as GPIO



GPIO.setmode(GPIO.BCM)


import TemperatureHumidityGraph 


TemperatureHumidityGraph.TemperatureHumidityGraph('test', 10, 0)

