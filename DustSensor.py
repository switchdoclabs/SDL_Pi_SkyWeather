#!/usr/bin/env python

#SwithchDoc Labs September 2018
# Public Domain


# tests SDL_Pi_DustSensor Driver
import sys
sys.path.append('./SDL_Pi_DustSensor')
import time
import pigpio
import SDL_Pi_DustSensor

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
# Check for user imports
try:
            import conflocal as config
except ImportError:
            import config

import state

def powerOnDustSensor():
        GPIO.setup(config.DustSensorPowerPin, GPIO.OUT)
        GPIO.output(config.DustSensorPowerPin, True)
        time.sleep(1)

def powerOffDustSensor():
        GPIO.setup(config.DustSensorPowerPin, GPIO.OUT)
        GPIO.output(config.DustSensorPowerPin, False)
        time.sleep(1)


def read_AQI():

      if (config.SWDEBUG):
          print ("###############")
          print ("Reading AQI")
          print ("###############")

      if (config.SWDEBUG):
          print ("Turning Dust Power On")
      powerOnDustSensor()

      pi = pigpio.pi() # Connect to Pi.
   
      dustSensor = SDL_Pi_DustSensor.SDL_Pi_DustSensor(pi, config.DustSensorPin) # set the GPIO pin number

      # delay for 30 seconds for calibrated reading

      time.sleep(30)
      
      # get the gpio, ratio and concentration in particles / 0.01 ft3
      g, r, c = dustSensor.read()

      # concentration above 1,080,000 considered error
      if (c>=1080000.00):
          if (config.SWDEBUG):
            print("Dust Sensor Concentration Error\n")

      if (config.SWDEBUG):
        print("Air Quality Measurements for PM2.5:")
        print("  " + str(int(c)) + " particles/0.01ft^3")

      # convert to SI units
      concentration_ugm3=dustSensor.pcs_to_ugm3(c)
      if (config.SWDEBUG):
        print("  " + str(int(concentration_ugm3)) + " ugm^3")
      
      # convert SI units to US AQI
      # input should be 24 hour average of ugm3, not instantaneous reading
      aqi=dustSensor.ugm3_to_aqi(concentration_ugm3)
      
      if (config.SWDEBUG):
        print("  Current AQI (not 24 hour avg): " + str(int(aqi)))
        print("")

      state.Outdoor_AirQuality_Sensor_Value = int(aqi)
      pi.stop() # Disconnect from Pi.

      if (config.SWDEBUG):
          print ("Turning Dust Sensor Power Off")
      powerOffDustSensor()


