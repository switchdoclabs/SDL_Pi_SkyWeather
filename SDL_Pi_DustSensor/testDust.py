#!/usr/bin/env python

#SwithchDoc Labs September 2018
# Public Domain

import pigpio

# tests SDL_Pi_DustSensor Driver

import time
import pigpio
import SDL_Pi_DustSensor

SENSORPIN = 4



while True:
      pi = pigpio.pi() # Connect to Pi.
   
      dustSensor = SDL_Pi_DustSensor.SDL_Pi_DustSensor(pi, SENSORPIN) # set the GPIO pin number

      # Use 30s for a properly calibrated reading.
      time.sleep(30) 
      
      # get the gpio, ratio and concentration in particles / 0.01 ft3
      g, r, c = dustSensor.read()

      # concentration above 1,080,000 considered error
      if (c>=1080000.00):
          print("Concentration Error\n")
          continue

      print("Air Quality Measurements for PM2.5:")
      print("  " + str(int(c)) + " particles/0.01ft^3")

      # convert to SI units
      concentration_ugm3=dustSensor.pcs_to_ugm3(c)
      print("  " + str(int(concentration_ugm3)) + " ugm^3")
      
      # convert SI units to US AQI
      # input should be 24 hour average of ugm3, not instantaneous reading
      aqi=dustSensor.ugm3_to_aqi(concentration_ugm3)
      
      print("  Current AQI (not 24 hour avg): " + str(int(aqi)))
      print("")

      pi.stop() # Disconnect from Pi.

      time.sleep(5)

