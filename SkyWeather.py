#
# SkyWeather Solar Powered Weather Station
# February 2019
#
# SwitchDoc Labs
# www.switchdoc.com
#
#

# imports
# Check for user imports
try:
	import conflocal as config
except ImportError:
	import config

config.SWVERSION = "055"


import sys
import time
import traceback

from datetime import datetime

import random 
import re
import math
import os
import threading
import commands

import sendemail
import logging
logging.basicConfig()

import pclogging

import updateBlynk

import state


sys.path.append('./TSL2591')
sys.path.append('./SDL_Pi_SI1145')
sys.path.append('./SDL_Pi_TCA9545')

sys.path.append('./SDL_Pi_SSD1306')
sys.path.append('./Adafruit_Python_SSD1306')
sys.path.append('./RTC_SDL_DS3231')
sys.path.append('./Adafruit_Python_BMP')
sys.path.append('./Adafruit_Python_GPIO')
sys.path.append('./SDL_Pi_WeatherRack')
sys.path.append('./RaspberryPi-AS3935/RPi_AS3935')
sys.path.append('./SDL_Pi_INA3221')
sys.path.append('./graphs')
sys.path.append('./SDL_Pi_HDC1000')
sys.path.append('./SDL_Pi_AM2315')
sys.path.append('./SDL_Pi_SHT30')
sys.path.append('./BME680')

sys.path.append('./SDL_Pi_GrovePowerDrive')

import subprocess
import RPi.GPIO as GPIO
import doAllGraphs
import smbus

import struct

import SDL_Pi_HDC1000


from apscheduler.schedulers.background import BackgroundScheduler

import apscheduler.events

if (config.enable_MySQL_Logging == True):
	import MySQLdb as mdb

import picamera

import SkyCamera

import DustSensor

import util

################
# Device Present State Variables
###############

#indicate interrupt has happened from as3936

as3935_Interrupt_Happened = False;

config.Camera_Present = False
config.TCA9545_I2CMux_Present = False
config.SunAirPlus_Present = False
config.AS3935_Present = False
config.DS3231_Present = False
config.BMP280_Present = False
config.BME680_Present = False
config.AM2315_Present = False
config.ADS1015_Present = False
config.ADS1115_Present = False
config.OLED_Present = False
config.WXLink_Present = False
config.Sunlight_Present = False
config.TSL2591_Present = False
config.SolarMax_Present = False

# if the WXLink has stopped transmitting, == False
config.WXLink_Data_Fresh = False
config.WXLink_LastMessageID = 0

import SDL_Pi_INA3221
import SDL_DS3231
import Adafruit_BMP.BMP280 as BMP280
import SDL_Pi_WeatherRack as SDL_Pi_WeatherRack
import bme680 as BME680
import BME680_Functions

from RPi_AS3935 import RPi_AS3935


import Adafruit_SSD1306

import Scroll_SSD1306

import WeatherUnderground


import SDL_Pi_SI1145
import SI1145Lux

if (config.runLEDs):
    from neopixel import *
    import pixelDriver

import TSL2591
import SDL_Pi_TCA9545


################
#Establish WeatherSTEMHash
################
if (config.USEWEATHERSTEM == True):
    state.WeatherSTEMHash = SkyCamera.SkyWeatherKeyGeneration(config.STATIONKEY)

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
	tca9545.write_control_register(TCA9545_CONFIG_BUS2)
	config.TCA9545_I2CMux_Present = True
except:
	print ">>>>>>>>>>>>>>>>>>><<<<<<<<<<<"
	print "TCA9545 I2C Mux Not Present" 
	print ">>>>>>>>>>>>>>>>>>><<<<<<<<<<<"
	config.TCA9545_I2CMux_Present = False




def removePower(GroveSavePin):
        GPIO.setup(GroveSavePin, GPIO.OUT)
        GPIO.output(GroveSavePin, False)
        

def restorePower(GroveSavePin):
        GPIO.setup(GroveSavePin, GPIO.OUT)
        GPIO.output(GroveSavePin, True)
   
def togglePower(GroveSavePin):
        if (config.SWDEBUG == True):
            print("Toggling Power to Pin=", GroveSavePin)
        removePower(GroveSavePin)
        time.sleep(4.5)
        restorePower(GroveSavePin)



###############
# Fan Control
###############

import SDL_Pi_GrovePowerDrive

TEMPFANTURNON = 37.0
TEMPFANTURNOFF = 34.0

myPowerDrive = SDL_Pi_GrovePowerDrive.SDL_Pi_GrovePowerDrive(config.GPIO_Pin_PowerDrive_Sig1, config.GPIO_Pin_PowerDrive_Sig2, False, False)

def turnFanOn():
   if (state.fanState == False):
    pclogging.log(pclogging.INFO, __name__, "Turning Fan On" )
    if (config.USEBLYNK):
        updateBlynk.blynkStatusTerminalUpdate("Turning Fan On")
    myPowerDrive.setPowerDrive(1, True) 
    myPowerDrive.setPowerDrive(2, True) 
    state.fanState = True

def turnFanOff():
   if (state.fanState == True):
    pclogging.log(pclogging.INFO, __name__, "Turning Fan Off" )
    if (config.USEBLYNK):
       updateBlynk.blynkStatusTerminalUpdate("Turning Fan Off")
    myPowerDrive.setPowerDrive(1, False) 
    myPowerDrive.setPowerDrive(2, False)
    state.fanState = False
 

turnFanOff()



###############

# TSL2591 Sunlight Sensor Setup

################

# turn I2CBus 3 on
if (config.TCA9545_I2CMux_Present):
	 tca9545.write_control_register(TCA9545_CONFIG_BUS3)

try:
    tsl2591 = TSL2591.Tsl2591()
    int_time=TSL2591.INTEGRATIONTIME_100MS
    gain=TSL2591.GAIN_LOW
    tsl2591.set_gain(gain)
    tsl2591.set_timing(int_time)
    full, ir = tsl2591.get_full_luminosity()  # read raw values (full spectrum and ir spectrum)
    lux = tsl2591.calculate_lux(full, ir)  # convert raw values to lux
    print (lux, full, ir)
    print ()
    config.TSL2591_Present = True 

except:
    config.TSL2591_Present = False 



###############

# Sunlight SI1145 Sensor Setup

################
# turn I2CBus 3 on
if (config.TCA9545_I2CMux_Present):
	 tca9545.write_control_register(TCA9545_CONFIG_BUS3)

try:
        #restorePower(SI1145GSPIN)
        time.sleep(1.0)
	Sunlight_Sensor = SDL_Pi_SI1145.SDL_Pi_SI1145(indoor=0)
        time.sleep(1.0)

        visible = Sunlight_Sensor.readVisible() 
        print "visible=", visible
        config.Sunlight_Present = True
        vis = Sunlight_Sensor.readVisible()
       	IR = Sunlight_Sensor.readIR()
       	UV = Sunlight_Sensor.readUV()
       	IR_Lux = SI1145Lux.SI1145_IR_to_Lux(IR)
       	vis_Lux = SI1145Lux.SI1145_VIS_to_Lux(vis)
       	uvIndex = UV / 100.0
        if (visible == 0):
            time.sleep(1.0)
	    Sunlight_Sensor = SDL_Pi_SI1145.SDL_Pi_SI1145(indoor=0)
            time.sleep(1.0)
        time.sleep(1.0)



except:
        config.Sunlight_Present = False

def returnStatusLine(device, state):

        returnString = device
        if (state == True):
                returnString = returnString + ":   \t\tPresent"
        else:
                returnString = returnString + ":   \t\tNot Present"
        return returnString

###############
# Pixel Strip  LED
###############

# Create NeoPixel object with appropriate configuration.
#strip = Adafruit_NeoPixel(pixelDriver.LED_COUNT, pixelDriver.LED_PIN, pixelDriver.LED_FREQ_HZ, pixelDriver.LED_DMA, pixelDriver.LED_INVERT, pixelDriver.LED_BRIGHTNESS, pixelDriver.LED_CHANNEL, pixelDriver.LED_STRIP)
# Intialize the library (must be called once before other functions).
#strip.begin()
PixelLock = threading.Lock()



    
################
# PiCamera detect

try:

    with picamera.PiCamera() as cam:
            print("Pi Camera Revision",cam.revision)
            cam.close()
    config.Camera_Present = True
except:
    config.Camera_Present = False



# semaphore primitives for preventing I2C conflicts


I2C_Lock = threading.Lock()


################
# SunAirPlus Sensors


# the three channels of the INA3221 named for SunAirPlus Solar Power Controller channels (www.switchdoc.com)
LIPO_BATTERY_CHANNEL = 1
SOLAR_CELL_CHANNEL   = 2
OUTPUT_CHANNEL       = 3

try:
	if (config.TCA9545_I2CMux_Present):
         	# switch to BUS2 -  SunAirPlus is on Bus2
         	tca9545.write_control_register(TCA9545_CONFIG_BUS2)
        
	sunAirPlus = SDL_Pi_INA3221.SDL_Pi_INA3221(addr=0x40)

        busvoltage1 = sunAirPlus.getBusVoltage_V(LIPO_BATTERY_CHANNEL)
        config.SunAirPlus_Present = True
except:
        config.SunAirPlus_Present = False



SUNAIRLED = 25



################
# turn I2CBus 0 on
if (config.TCA9545_I2CMux_Present):
	 tca9545.write_control_register(TCA9545_CONFIG_BUS0)

# Check for HDC1080 first (both are on 0x40)


###############

# HDC1080 Detection
try:
	hdc1080 = SDL_Pi_HDC1000.SDL_Pi_HDC1000() 
        deviceID = hdc1080.readDeviceID() 
	print "deviceID = 0x%X" % deviceID
	if (deviceID == 0x1050):
        	config.HDC1080_Present = True
	else:
		config.HDC1080_Present = False
except:
        config.HDC1080_Present = False



###############

#WeatherRack Weather Sensors
#
# GPIO Numbering Mode GPIO.BCM
#


# constants

SDL_MODE_INTERNAL_AD = 0
SDL_MODE_I2C_ADS1015 = 1    # internally, the library checks for ADS1115 or ADS1015 if found

#sample mode means return immediately.  THe wind speed is averaged at sampleTime or when you ask, whichever is longer
SDL_MODE_SAMPLE = 0
#Delay mode means to wait for sampleTime and the average after that time.
SDL_MODE_DELAY = 1

# turn I2CBus 0 on
if (config.TCA9545_I2CMux_Present):
	tca9545.write_control_register(TCA9545_CONFIG_BUS0)
weatherStation = SDL_Pi_WeatherRack.SDL_Pi_WeatherRack(config.anemometerPin, config.rainPin, 0,0, SDL_MODE_I2C_ADS1015)

weatherStation.setWindMode(SDL_MODE_SAMPLE, 5.0)
#weatherStation.setWindMode(SDL_MODE_DELAY, 5.0)



################
# WXLink Setup

#resetWXLink()
sys.path.append('./pyRFM')
import lib as pyrfm

import readLoRa

try:
        
	

    conf={
	'll':{
		'type':'rfm95'
	},
	'pl':{
		'type':	'serial_seed',
		'port':	'/dev/ttyS0'
	}
    }


    state.ll=pyrfm.getLL(conf)

    if state.ll.setOpModeSleep(True,True):
	state.ll.setFiFo()
	state.ll.setOpModeIdle()
        state.ll.setModemConfig('Bw31_25Cr48Sf512');
	#state.ll.setModemConfig('Bw125Cr45Sf128');
	#state.ll.setPreambleLength(8)
	state.ll.setFrequency(434.0)
	state.ll.setTxPower(13)
	
        print('HW-Version: ', state.ll.getVersion())
        config.WXLink_Present = True

except:
        config.WXLink_Present = False

state.block1 = ""
state.block2 = ""


################
# DS3231/AT24C32 Setup
# turn I2CBus 0 on
if (config.TCA9545_I2CMux_Present):
         tca9545.write_control_register(TCA9545_CONFIG_BUS0)

filename = time.strftime("%Y-%m-%d%H:%M:%SRTCTest") + ".txt"
starttime = datetime.utcnow()

ds3231 = SDL_DS3231.SDL_DS3231(1, 0x68)


try:

        
        ds3231.write_now()
        ds3231.read_datetime()
        #print "DS3231=\t\t%s" % ds3231.read_datetime()
        config.DS3231_Present = True

except IOError as e:
        #print "I/O error({0}): {1}".format(e.errno, e.strerror)
        config.DS3231_Present = False



################

# BMP280 Setup 

try:
        bmp280 = BMP280.BMP280()
        config.BMP280_Present = True

except: 

        #    print "I/O error({0}): {1}".format(e.errno, e.strerror)
        config.BMP280_Present = False


################

# BME680 Setup 

try:
        bme680 = BME680.BME680(BME680.I2C_ADDR_SECONDARY)
        config.BME680_Present = True
        BME680_Functions.setup_bme680(bme680)
except IOError as e:

        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        config.BME680_Present = False

print ("after bme680", config.BME680_Present)



################

# OLED SSD_1306 Detection

try:
        RST =27
        display = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
        # Initialize library.
        display.begin()
        display.clear()
        display.display()
        config.OLED_Present = True
        config.OLED_Originally_Present = True
except:
        config.OLED_Originally_Present = False
        config.OLED_Present = False

def initializeOLED():
    try:
        RST =27
        display = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
        # Initialize library.
        display.begin()
        display.clear()
        display.display()
        config.OLED_Present = True
        config.OLED_Originally_Present = True
    except:
        config.OLED_Originally_Present = False
        config.OLED_Present = False




################
def process_as3935_interrupt():

    global as3935Interrupt
    global as3935, as3935LastInterrupt, as3935LastDistance, as3935LastStatus

    as3935Interrupt = False

    print "processing Interrupt from as3935"
    # turn I2CBus 1 on for low loading
    if (config.TCA9545_I2CMux_Present):
         tca9545.write_control_register(TCA9545_CONFIG_BUS1)
    time.sleep(0.020)
    reason = as3935.get_interrupt()

    as3935LastInterrupt = reason
    
    if reason == 0x00:
	as3935LastStatus = "Spurious Interrupt"
        if (config.USEBLYNK):
            updateBlynk.blynkStatusTerminalUpdate("AS3935: Spurious Interrupt")
    elif reason == 0x01:
	as3935LastStatus = "Noise Floor too low. Adjusting"
        if (config.USEBLYNK):
            updateBlynk.blynkStatusTerminalUpdate("AS3935: Noise Floor too low - adjusted")
        as3935.raise_noise_floor()
    elif reason == 0x04:
	as3935LastStatus = "Disturber detected - masking"
        if (config.USEBLYNK):
            updateBlynk.blynkStatusTerminalUpdate("AS3935: Disturber detected - masking")
        as3935.set_mask_disturber(True)
    elif reason == 0x08:
        now = datetime.now().strftime('%H:%M:%S - %Y/%m/%d')
        distance = as3935.get_distance()
	as3935LastDistance = distance
	as3935LastStatus = "Lightning Detected "  + str(distance) + "km away. (%s)" % now
        if (config.USEBLYNK):
            updateBlynk.blynkEventUpdate("Lightning Detected "  + str(distance) + "km away.")
            updateBlynk.blynkStatusTerminalUpdate("Lightning Detected "  + str(distance) + "km away.")

	pclogging.log(pclogging.INFO, __name__, "Lightning Detected "  + str(distance) + "km away. (%s)" % now)
        if (config.enableText):
	    sendemail.sendEmail("test", config.STATIONKEY + " Lightning Detected\n", as3935LastStatus, config.textnotifyAddress,  config.fromAddress, "");
        # now set LED parameters
        state.currentAs3935LastLightningTimeStamp = time.time()
    
    state.currentAs3935LastDistance = as3935LastDistance 
    state.currentAs3935LastStatus = as3935LastStatus 
    state.currentAs3935Interrupt = as3935LastInterrupt 
    
    print "Last Interrupt = 0x%x:  %s" % (as3935LastInterrupt, as3935LastStatus)
    if (config.TCA9545_I2CMux_Present):
         tca9545.write_control_register(TCA9545_CONFIG_BUS1)

    time.sleep(0.003)



# as3935 Set up Lightning Detector
as3935LastInterrupt = 0
as3935LightningCount = 0
as3935LastDistance = 0
as3935LastStatus = ""
as3935Interrupt = False



# switch to BUS1 - for low loading ib Base Bus
if (config.TCA9545_I2CMux_Present):
   	tca9545.write_control_register(TCA9545_CONFIG_BUS1)

as3935 = RPi_AS3935(address=0x02, bus=1)

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

                print "as3935 start"

                as3935.set_noise_floor(NoiseFloor)
                as3935.set_indoors(Indoor)
                as3935.calibrate(tun_cap=TuneCap)
                as3935.set_mask_disturber(DisturberDetection)
                as3935.set_watchdog_threshold(WatchDogThreshold)
                as3935.set_spike_detection(SpikeDetection)


                config.AS3935_Present = True
                print "as3935 present at 0x02"
		#process_as3935_interrupt()
                if (config.TCA9545_I2CMux_Present):
         	    tca9545.write_control_register(TCA9545_CONFIG_BUS1)

except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
        	as3935 = RPi_AS3935(address=0x03, bus=1)

        	try:

                        as3935.set_noise_floor(NoiseFloor)
                        as3935.set_indoors(Indoor)
                        as3935.calibrate(tun_cap=TuneCap)
                        as3935.set_mask_disturber(DisturberDetection)
                        as3935.set_watchdog_threshold(WatchDogThreshold)
                        as3935.set_spike_detection(SpikeDetection)

                	config.AS3935_Present = True
                	#print "as3935 present"
        	except IOError as e:

               		print "I/O error({0}): {1}".format(e.errno, e.strerror)
                	config.AS3935_Present = False
                	# back to BUS0
                	if (config.TCA9545_I2CMux_Present):
        		 	tca9545.write_control_register(TCA9545_CONFIG_BUS0)



# back to BUS0
if (config.TCA9545_I2CMux_Present):
        	 tca9545.write_control_register(TCA9545_CONFIG_BUS0)
time.sleep(0.003)




def handle_as3935_interrupt(channel):
    global as3935Interrupt

    print "as3935 Interrupt"

    as3935Interrupt = True


# define Interrupt Pin for AS3935
as3935pin = 16 

#GPIO.setup(as3935pin, GPIO.IN)
GPIO.setup(as3935pin, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(as3935pin, GPIO.RISING, callback=handle_as3935_interrupt)


##############
# Setup SHT30
# turn I2CBus 0 on
if (config.TCA9545_I2CMux_Present):
         tca9545.write_control_register(TCA9545_CONFIG_BUS0)

# Grove Power Save Pins for device reset

###############

# Detect SHT30
outsideHumidity = 0.0
outsideTemperature = 0.0
crc_check = -1
import SHT30
try:
 	sht30 = SHT30.SHT30(powerpin=config.SHT30GSPIN )
	outsideHumidity, outsideTemperature, crc_checkH, crc_checkT = sht30.fast_read_humidity_temperature_crc() 
	
	print "outsideTemperature: %0.1f C" % outsideTemperature
    	print "outsideHumidity: %0.1f %%" % outsideHumidity
        state.currentOutsideTemperature = outsideTemperature
        state.currentOutsideHumidity = outsideHumidity
        print "crcH: 0x%02x" % crc_checkH
        print "crcT 0x%02x" % crc_checkT
        config.SHT30_Present = True
        if (crc_checkH == -1) or (crc_checkT == -1):
        	config.SHT30_Present = False

except Exception as e:

        config.SHT30_Present = False

        #print "exception in SHT30 Check"
        #print(traceback.format_exc())
        #print (e)



print "after SHT30"


##############
# Setup AM2315
# turn I2CBus 0 on
if (config.TCA9545_I2CMux_Present):
         tca9545.write_control_register(TCA9545_CONFIG_BUS0)

# Grove Power Save Pins for device reset

if (config.SHT30_Present == False):  # don't check for AM2315 if you find SHT30

    ###############

    # Detect AM2315
    outsideHumidity = 0.0
    outsideTemperature = 0.0
    crc_check = -1
    import AM2315
    try:
 	    am2315 = AM2315.AM2315(powerpin=config.AM2315GSPIN )
	    outsideHumidity, outsideTemperature, crc_check = am2315.read_humidity_temperature_crc() 
	    #outsideHumidity, outsideTemperature, crc_check = am2315.fast_read_humidity_temperature_crc() 
	    print "outsideTemperature: %0.1f C" % outsideTemperature
    	    print "outsideHumidity: %0.1f %%" % outsideHumidity
            state.currentOutsideTemperature = outsideTemperature
            state.currentOutsideHumidity = outsideHumidity
            print "crc: 0x%02x" % crc_check
            config.AM2315_Present = True
            if (crc_check == -1):
        	    config.AM2315_Present = False

    except:
            config.AM2315_Present = False





# Main Program




# write SunAirPlus stats out to file
def writeSunAirPlusStats():

        f = open("/home/pi/SDL_Pi_SkyWeather/state/SunAirPlusStats.txt", "w")
	f.write(str(batteryVoltage) + '\n')
	f.write(str(batteryCurrent ) + '\n')
	f.write(str(solarVoltage) + '\n')
	f.write(str(solarCurrent ) + '\n')
	f.write(str(loadVoltage ) + '\n')
	f.write(str(loadCurrent) + '\n')
	f.write(str(batteryPower ) + '\n')
	f.write(str(solarPower) + '\n')
	f.write(str(loadPower) + '\n')
	f.write(str(batteryCharge) + '\n')
        f.close()

# write weather stats out to file
def writeWeatherStats():

        f = open("/home/pi/SDL_Pi_SkyWeather/state/WeatherStats.txt", "w")
	f.write(str(totalRain) + '\n') 
	f.write(str(as3935LightningCount) + '\n')
	f.write(str(as3935LastInterrupt) + '\n')
	f.write(str(as3935LastDistance) + '\n')
	f.write(str(as3935LastStatus) + '\n')
 	f.write(str(currentWindSpeed) + '\n')
	f.write(str(currentWindGust) + '\n')
	f.write(str(totalRain)  + '\n')
  	f.write(str(bmp180Temperature)  + '\n')
	f.write(str(bmp180Pressure) + '\n')
	f.write(str(bmp180Altitude) + '\n')
	f.write(str(bmp180SeaLevel)  + '\n')
    	f.write(str(outsideTemperature) + '\n')
	f.write(str(outsideHumidity) + '\n')
	f.write(str(currentWindDirection) + '\n')
	f.write(str(currentWindDirectionVoltage) + '\n')
	f.write(str(HTUtemperature) + '\n')
	f.write(str(HTUhumidity) + '\n')
        f.close()



# sample weather 
totalRain = 0
def sampleWeather():

	global as3935LightningCount
    	global as3935, as3935LastInterrupt, as3935LastDistance, as3935LastStatus
 	global currentWindSpeed, currentWindGust, totalRain 
  	global 	bmp180Temperature, bmp180Pressure, bmp180Altitude,  bmp180SeaLevel 
    	global outsideTemperature, outsideHumidity, crc_check 
	global currentWindDirection, currentWindDirectionVoltage

        global	SunlightVisible, SunlightIR, SunlightUV,  SunlightUVIndex 

	global HTUtemperature, HTUhumidity, rain60Minutes


        global am2315



	print "----------------- "
	print " Weather Sampling" 
	print "----------------- "
	#
	# turn I2CBus 0 on
 	if (config.TCA9545_I2CMux_Present):
         	tca9545.write_control_register(TCA9545_CONFIG_BUS0)
	SDL_INTERRUPT_CLICKS = 1

	if ((config.WXLink_Present == False) or ((config.SolarMAX_Present == True) and (config.WXLink_Present == True) and (config.Dual_MAX_WXLink == False))):
 		currentWindSpeed = weatherStation.current_wind_speed()
  		currentWindGust = weatherStation.get_wind_gust()
  		totalRain = totalRain + weatherStation.get_current_rain_total()/SDL_INTERRUPT_CLICKS
		if ((config.ADS1015_Present == True) or (config.ADS1115_Present == True)):
			currentWindDirection = weatherStation.current_wind_direction()
			currentWindDirectionVoltage = weatherStation.current_wind_direction_voltage()

	if (config.WXLink_Present == True):

		# WXLink Data Gathering
                #pay attention to semaphore in case new block is coming in

	        returnList = readLoRa.readWXLink(state.block1, state.block2, state.stringblock1, state.stringblock2, state.block1_orig, state.block2_orig)

                  	
                if (len(returnList) > 0):
                    # OK, clear blocks - we have interpreted them
                    state.block1 = []
                    state.block2 = []
                    state.stringblock1 = ""
                    state.stringblock2 = ""
                    state.block1_orig = []
                    state.block2_orig = []


                    protocol_ID = returnList[0]

                    if (protocol_ID == 3):   # WXLink Packet
 	
                      if ((config.Dual_MAX_WXLink == True) or (config.SolarMAX_Present == False)):
		
		
	
			currentWindSpeed = returnList[3]
  			currentWindGust = 0.0 # not supported
  			totalRain = returnList[5]
			currentWindDirection = returnList[6]
			currentWindDirectionVoltage =  0.0 # not supported

    			outsideTemperature = returnList[7]
    			outsideHumidity = returnList[8]

                        if ((config.SunAirPlus_Present == False) and (config.SolarMAX_Present == False)): # if SunAirPlus or SolarMAX not here, use WXLink data
                            state.batteryVoltage = state.WXbatteryVoltage 
                            state.batteryCurrent = state.WXbatteryCurrent
                            state.solarVoltage = state.WXsolarVoltage
                            state.solarCurrent = state.WXsolarCurrent
                            state.loadVoltage = state.WXloadVoltage
                            state.loadCurrent = state.WXloadCurrent
                            state.batteryPower = state.WXbatteryPower
                            state.solarPower = state.WXsolarPower
                            state.loadPower = state.WXloadPower
                            state.batteryCharge = state.WXbatteryCharge
                        if (config.USEBLYNK):
                            if (config.WXLink_Data_Fresh == True):
                                updateBlynk.blynkStatusTerminalUpdate("WXLink ID# %d recieved"%config.WXLink_LastMessageID)
                    else:
                        if (protocol_ID == 8): # do SolarMAX
                                pass # variable setting done in readLoRa


		else:  #if (len(returnList) > 0):
                    if (config.WXLink_Present == True):
	                if ((config.Dual_MAX_WXLink == True) or (config.SolarMAX_Present == False)):
			    currentWindSpeed = state.ScurrentWindSpeed  
  			    currentWindGust = 0.0 # not supported
  			    totalRain = state.currentTotalRain
			    currentWindDirection = state.ScurrentWindDirection
			    currentWindDirectionVoltage = 0.0 # not supported
    
    			    outsideTemperature = state.currentOutsideTemperature
    			    outsideHumidity = state.currentOutsideHumidity
			    # checks for issue on startup
			    if ((len(state.block1) == 0) or (len(state.block2) == 0)):

				# skip update if bad
				currentWindSpeed = 0.0 
  				currentWindGust = 0.0 # not supported
  				totalRain = 0.0 
				currentWindDirection = 0
				currentWindDirectionVoltage =  0.0 # not supported
	
    				outsideTemperature = 0.0 
    				outsideHumidity =  0.0

			print "Bad data from WXLink, discarded new data.  Kept old"
		
        print "----------------- "
  
	if (config.BMP280_Present):	
		try:
			bmp180Temperature = bmp280.read_temperature()
			bmp180Pressure = bmp280.read_pressure()/1000
			bmp180Altitude = bmp280.read_altitude()
			bmp180SeaLevel = bmp280.read_sealevel_pressure(config.BMP280_Altitude_Meters)/1000
		except:
        		print("Unexpected error:", sys.exc_info()[0])


	if (config.BME680_Present):	
		try:
			data = bme680.get_sensor_data()
			bmp180Temperature = bme680.data.temperature
                        bmp180Humidity = bme680.data.humidity
			bmp180Pressure = bme680.data.pressure
			bmp180Altitude = config.BMP280_Altitude_Meters 
			bmp180SeaLevel = BME680_Functions.getSeaLevelPressure(config.BMP280_Altitude_Meters, bmp180Pressure)
                        # reset read pressure to Sea Level
                        #bmp180Pressure = bmp180SeaLevel 

		except:
        		print("Unexpected error:", sys.exc_info()[0])


	HTUtemperature = 0.0
	HTUhumidity = 0.0


	if (config.HDC1080_Present):
		
		HTUtemperature = hdc1080.readTemperature() 
		HTUhumidity =  hdc1080.readHumidity()

        else:

		HTUtemperature = bmp180Temperature
		HTUhumidity =  bmp180Humidity



        # use TSL2591 first

        if (config.TSL2591_Present):
	    ################
	    # turn I2CBus 3 on
	    if (config.TCA9545_I2CMux_Present):
	 	tca9545.write_control_register(TCA9545_CONFIG_BUS3)

            full, ir = tsl2591.get_full_luminosity()  # read raw values (full spectrum and ir spectrum)
            lux = tsl2591.calculate_lux(full, ir)  # convert raw values to lux
            SunlightVisible = lux
            SunlightIR = ir 
            SunlightUV = 0
            SunlightUVIndex = 0.0
            

        else:
	    if (config.Sunlight_Present):
		################
		# turn I2CBus 3 on
		if (config.TCA9545_I2CMux_Present):
	 		tca9545.write_control_register(TCA9545_CONFIG_BUS3)

        	SunlightVisible = SI1145Lux.SI1145_VIS_to_Lux(Sunlight_Sensor.readVisible())
        	SunlightIR = SI1145Lux.SI1145_IR_to_Lux(Sunlight_Sensor.readIR())
        	SunlightUV = Sunlight_Sensor.readUV()
        	SunlightUVIndex = SunlightUV / 100.0
		################
		# turn I2CBus 0 on
		if (config.TCA9545_I2CMux_Present):
	 		tca9545.write_control_register(TCA9545_CONFIG_BUS0)

	    else:
        	SunlightVisible = 0
        	SunlightIR = 0 
        	SunlightUV = 0
        	SunlightUVIndex = 0.0



	if (as3935LastInterrupt == 0x00):
		as3935InterruptStatus = "----No Lightning detected---"
		
	if (as3935LastInterrupt == 0x01):
		as3935InterruptStatus = "Noise Floor: %s" % as3935LastStatus
		as3935LastInterrupt = 0x00

	if (as3935LastInterrupt == 0x04):
		as3935InterruptStatus = "Disturber: %s" % as3935LastStatus
		as3935LastInterrupt = 0x00

	if (as3935LastInterrupt == 0x08):
		as3935InterruptStatus = "Lightning: %s" % as3935LastStatus
		as3935LightningCount += 1
		as3935LastInterrupt = 0x00


	if (config.AS3935_Present):
		as3935InterruptStatus = "No AS3935 Lightning Detector Present"
		as3935LastInterrupt = 0x00
		
	if (config.WXLink_Present == False) : # do not use internal AM2315 or SHT30 if we are WXLink connected
           # if both AM2315 and SHT30 are present, SHT30 wins
	   if (config.AM2315_Present) and ( config.SHT30_Present == False):
		# get AM2315 Outside Humidity and Outside Temperature
		# turn I2CBus 0 on
 		if (config.TCA9545_I2CMux_Present):
        		 tca9545.write_control_register(TCA9545_CONFIG_BUS0)

                try:
    		    ToutsideHumidity, ToutsideTemperature, crc_check = am2315.read_humidity_temperature_crc()
                except:
                     if am2315 is None:
		        am2315 = AM2315.AM2315(powerpin=config.AM2315GSPIN )
                        print ("am2315 None Error Detected")
                     crc_check = -1

		if (crc_check !=  -1):
                    outsideTemperature = ToutsideTemperature
                    outsideHumidity = ToutsideHumidity
                    state.currentOutsideTemperature = outsideTemperature
                    state.currentOutsideHumidity = outsideHumidity
	        if (config.SWDEBUG == True):
                    print "AM2315 Stats: (g,br,bc,rt,pc)", am2315.read_status_info()

           # if both AM2315 and SHT30 are present, SHT30 wins
	   if (config.SHT30_Present):
		# get SHT30 Outside Humidity and Outside Temperature
		# turn I2CBus 0 on
 		if (config.TCA9545_I2CMux_Present):
        		 tca9545.write_control_register(TCA9545_CONFIG_BUS0)

    		ToutsideHumidity, ToutsideTemperature, crc_checkH, crc_checkT = sht30.read_humidity_temperature_crc()
                

		if (crc_checkH !=  -1) and (crc_checkT != -1):
                    outsideTemperature = ToutsideTemperature
                    outsideHumidity = ToutsideHumidity
                    state.currentOutsideTemperature = outsideTemperature
                    state.currentOutsideHumidity = outsideHumidity
	        if (config.SWDEBUG == True):
                    print "SHT30 Stats: (g,br,bc,rt,pc)", sht30.read_status_info()

        else:   # WXLink == True if SolarMAX is here and WXLink is not, the read AM2315/SHT30
            if ((config.SolarMAX_Present == True) and (config.Dual_MAX_WXLink == False)):

                # if both AM2315 and SHT30 are present, SHT30 wins
	        if (config.AM2315_Present) and ( config.SHT30_Present == False):
		        # get AM2315 Outside Humidity and Outside Temperature
		        # turn I2CBus 0 on
 		        if (config.TCA9545_I2CMux_Present):
        		        tca9545.write_control_register(TCA9545_CONFIG_BUS0)

                        try:
    		            ToutsideHumidity, ToutsideTemperature, crc_check = am2315.read_humidity_temperature_crc()
                        except:
                            if am2315 is None:
		                am2315 = AM2315.AM2315(powerpin=config.AM2315GSPIN )
                                print ("am2315 None Error Detected")
                            crc_check = -1
        
		        if (crc_check !=  -1):
                            outsideTemperature = ToutsideTemperature
                            outsideHumidity = ToutsideHumidity
                            state.currentOutsideTemperature = outsideTemperature
                            state.currentOutsideHumidity = outsideHumidity
	                if (config.SWDEBUG == True):
                            print "AM2315 Stats: (g,br,bc,rt,pc)", am2315.read_status_info()

                # if both AM2315 and SHT30 are present, SHT30 wins
	        if (config.SHT30_Present):
		        # get SHT30 Outside Humidity and Outside Temperature
		        # turn I2CBus 0 on
 		        if (config.TCA9545_I2CMux_Present):
        		        tca9545.write_control_register(TCA9545_CONFIG_BUS0)
        
    		        ToutsideHumidity, ToutsideTemperature, crc_checkH, crc_checkT = sht30.read_humidity_temperature_crc()
                     
        
		        if (crc_checkH !=  -1) and (crc_checkT != -1):
                            outsideTemperature = ToutsideTemperature
                            outsideHumidity = ToutsideHumidity
                            state.currentOutsideTemperature = outsideTemperature
                            state.currentOutsideHumidity = outsideHumidity
	                if (config.SWDEBUG == True):
                            print "SHT30 Stats: (g,br,bc,rt,pc)", sht30.read_status_info()

	if (config.WeatherUnderground_Present == True):

		if (config.WXLink_Present):
			if (config.WXLink_Data_Fresh):
				# continue with send to WeatherUnderground
				print "WXLink_Data fresh and present"
			else:
				# data is not fresh, so don't send to WeatherUnderground
				print "WXLink_Data Stale don't send to WeatherUnderground"
				return

		# always set message stale set to False since we have consumed it
		config.WXLink_Data_Fresh = False

		try:
			print "--Sending Data to WeatherUnderground--"
			WeatherUnderground.sendWeatherUndergroundData( as3935LightningCount, as3935, as3935LastInterrupt, as3935LastDistance, as3935LastStatus, currentWindSpeed, currentWindGust, totalRain, bmp180Temperature, bmp180SeaLevel, bmp180Altitude,  bmp180SeaLevel, outsideTemperature, outsideHumidity, crc_check, currentWindDirection, currentWindDirectionVoltage, HTUtemperature, HTUhumidity, rain60Minutes)
		except:
			print "--WeatherUnderground Data Send Failed"

	else:
		# set the Data to stale  
		config.WXLink_Data_Fresh = False

        
        sampleSunAirPlus()

        # set State Variables

        # Weather Variables
        state.currentOutsideTemperature = outsideTemperature 
        state.currentOutsideHumidity = outsideHumidity 

        state.currentInsideTemperature = bmp180Temperature
        state.currentInsideHumidity = bmp180Humidity 

        state.currentRain60Minutes =  rain60Minutes

        state.currentSunlightVisible = SunlightVisible
        state.currentSunlightIR = SunlightIR
        state.currentSunlightUV = SunlightUV
        state.currentSunlightUVIndex  = SunlightUVIndex

        state.ScurrentWindSpeed = currentWindSpeed
        state.ScurrentWindGust  = currentWindGust
        state.ScurrentWindDirection  = currentWindDirection
        state.currentTotalRain  = totalRain

        state.currentBarometricPressure = bmp180Pressure 

        state.currentAltitude = bmp180Altitude
        state.currentSeaLevel = bmp180SeaLevel


        # check for turn fan on
        if (state.currentInsideTemperature > TEMPFANTURNON):
            turnFanOn()
        # check for turn fan off
        if (state.currentInsideTemperature < TEMPFANTURNOFF):
            turnFanOff()

	# turn I2CBus 0 on
 	if (config.TCA9545_I2CMux_Present):
         	tca9545.write_control_register(TCA9545_CONFIG_BUS0)


def sampleSunAirPlus():

	global batteryVoltage, batteryCurrent, solarVoltage, solarCurrent, loadVoltage, loadCurrent
	global batteryPower, solarPower, loadPower, batteryCharge


	if (config.SunAirPlus_Present):
		
		# turn I2CBus 2 on
 		if (config.TCA9545_I2CMux_Present):
        		 tca9545.write_control_register(TCA9545_CONFIG_BUS2)


		print "----------------- "
		print " SunAirPlus Sampling" 
		print "----------------- "
	

	
        	busvoltage1 = sunAirPlus.getBusVoltage_V(LIPO_BATTERY_CHANNEL)
        	shuntvoltage1 = sunAirPlus.getShuntVoltage_mV(LIPO_BATTERY_CHANNEL)
        	# minus is to get the "sense" right.   - means the battery is charging, + that it is discharging
        	batteryCurrent = sunAirPlus.getCurrent_mA(LIPO_BATTERY_CHANNEL)
        	batteryVoltage = busvoltage1 + (shuntvoltage1 / 1000)
		batteryPower = batteryVoltage * (batteryCurrent/1000)


        	busvoltage2 = sunAirPlus.getBusVoltage_V(SOLAR_CELL_CHANNEL)
        	shuntvoltage2 = sunAirPlus.getShuntVoltage_mV(SOLAR_CELL_CHANNEL)
        	solarCurrent = -sunAirPlus.getCurrent_mA(SOLAR_CELL_CHANNEL)
        	solarVoltage = busvoltage2 + (shuntvoltage2 / 1000)
		solarPower = solarVoltage * (solarCurrent/1000)

        	busvoltage3 = sunAirPlus.getBusVoltage_V(OUTPUT_CHANNEL)
        	shuntvoltage3 = sunAirPlus.getShuntVoltage_mV(OUTPUT_CHANNEL)
        	loadCurrent = sunAirPlus.getCurrent_mA(OUTPUT_CHANNEL)
        	loadVoltage = busvoltage3 
		loadPower = loadVoltage * (loadCurrent/1000)

		batteryCharge = util.returnPercentLeftInBattery(batteryVoltage, 4.19)	

                state.batteryVoltage = batteryVoltage 
                state.batteryCurrent = batteryCurrent
                state.solarVoltage = solarVoltage
                state.solarCurrent = solarCurrent
                state.loadVoltage = loadVoltage
                state.loadCurrent = loadCurrent
                state.batteryPower = batteryPower
                state.solarPower = solarPower
                state.loadPower = loadPower
                state.batteryCharge = batteryCharge
	else:
	
		print "----------------- "
		print " SunAirPlus Not Present" 
		print "----------------- "

def sampleAndDisplay():
        
    global currentWindSpeed, currentWindGust, totalRain
    global  bmp180Temperature, bmp180Pressure, bmp180Altitude,  bmp180SeaLevel
    global outsideTemperature, outsideHumidity, crc_check
    global currentWindDirection, currentWindDirectionVoltage

    global HTUtemperature, HTUhumidity

    global	SunlightVisible, SunlightIR, SunlightUV,  SunlightUVIndex 

    global totalRain, as3935LightningCount
    global as3935, as3935LastInterrupt, as3935LastDistance, as3935LastStatus

    I2C_Lock.acquire()

    try:

	print "----------------- "
	print " Sample and Display "
	print "----------------- "

        sampleWeather()

        state.pastBarometricReading = state.currentBarometricPressure

        if (config.OLED_Present):
                Scroll_SSD1306.addLineOLED(display,  ("Wind Speed=\t%0.2f MPH")%(currentWindSpeed/1.6))
                Scroll_SSD1306.addLineOLED(display,  ("Rain Total=\t%0.2f in")%(totalRain/25.4))
                if (config.ADS1015_Present or config.ADS1115_Present):
                        Scroll_SSD1306.addLineOLED(display,  "Wind Dir=%0.2f Degrees" % weatherStation.current_wind_direction())
	
	print "----------------- "
        print "----------------- "
        print "----------------- "
        #

        if (config.DS3231_Present == True):
                currenttime = datetime.utcnow()

                deltatime = currenttime - starttime

                print "Raspberry Pi=\t" + time.strftime("%Y-%m-%d %H:%M:%S")

                if (config.OLED_Present):
                        Scroll_SSD1306.addLineOLED(display,"%s" % ds3231.read_datetime())

                print "DS3231=\t\t%s" % ds3231.read_datetime()

                print "DS3231 Temperature= \t%0.2f C" % ds3231.getTemp()
                print "----------------- "





        if (config.HDC1080_Present):
                if (config.OLED_Present):
                        Scroll_SSD1306.addLineOLED(display,  "InTemp = \t%0.2f C" % HTUtemperature)


	if (config.AS3935_Present):
		print " AS3935 Lightning Detector "
	else:
		print " AS3935 Lightning Detector Not Present "

	print "----------------- "

	if (config.AS3935_Present):
		print "Last result from AS3935:"

		if (as3935LastInterrupt == 0x00):
			print "----No Lightning detected---"
		
		if (as3935LastInterrupt == 0x01):
			print "Noise Floor: %s" % as3935LastStatus
			as3935LastInterrupt = 0x00

		if (as3935LastInterrupt == 0x04):
			print "Disturber: %s" % as3935LastStatus
			as3935LastInterrupt = 0x00

		if (as3935LastInterrupt == 0x08):
			print "Lightning: %s" % as3935LastStatus
	        	if (config.OLED_Present):
                       	         Scroll_SSD1306.addLineOLED(display, '')
                       	         Scroll_SSD1306.addLineOLED(display, '---LIGHTNING---')
                                 Scroll_SSD1306.addLineOLED(display, '')
			as3935LightningCount += 1
			as3935LastInterrupt = 0x00

		print "Lightning Count = ", as3935LightningCount

	print "----------------- "
        
        if (config.SWDEBUG == True):
            state.printState()


        if (config.USEBLYNK):
           updateBlynk.blynkStateUpdate()
        
	print "----------------- "
	print " Sample and Display Done"
	print "----------------- "
    except IOError as e:

      print "I/O error({0}): {1}".format(e.errno, e.strerror)
      print "exception in Sample and Display Check"
      print(traceback.format_exc())
      

    I2C_Lock.release()


def writeWeatherRecord():
	global as3935LightningCount
    	global as3935, as3935LastInterrupt, as3935LastDistance, as3935LastStatus
 	global currentWindSpeed, currentWindGust, totalRain 
  	global 	bmp180Temperature, bmp180Pressure, bmp180Altitude,  bmp180SeaLevel 
    	global outsideTemperature, outsideHumidity, crc_check 
	global currentWindDirection, currentWindDirectionVoltage

        global	SunlightVisible, SunlightIR, SunlightUV,  SunlightUVIndex 

	global HTUtemperature, HTUhumidity



	# now we have the data, stuff it in the database

	try:
		print("trying database")
    		con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SkyWeather');

    		cur = con.cursor()
		print "before query"

		#query = 'INSERT INTO WeatherData(TimeStamp,as3935LightningCount, as3935LastInterrupt, as3935LastDistance, as3935LastStatus, currentWindSpeed, currentWindGust, totalRain,  bmp180Temperature, bmp180Pressure, bmp180Altitude,  bmp180SeaLevel,  outsideTemperature, outsideHumidity, currentWindDirection, currentWindDirectionVoltage, insideTemperature, insideHumidity, AQI) VALUES(UTC_TIMESTAMP(), %.3f, %.3f, %.3f, "%s", %.3f, %.3f, %.3f, %i, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)' % (as3935LightningCount, as3935LastInterrupt, as3935LastDistance, as3935LastStatus, currentWindSpeed, currentWindGust, totalRain,  bmp180Temperature, bmp180Pressure, bmp180Altitude,  bmp180SeaLevel,  outsideTemperature, outsideHumidity, currentWindDirection, currentWindDirectionVoltage, HTUtemperature, HTUhumidity, state.Outdoor_AirQuality_Sensor_Value)
		query = 'INSERT INTO WeatherData(TimeStamp,as3935LightningCount, as3935LastInterrupt, as3935LastDistance, as3935LastStatus, currentWindSpeed, currentWindGust, totalRain,  bmp180Temperature, bmp180Pressure, bmp180Altitude,  bmp180SeaLevel,  outsideTemperature, outsideHumidity, currentWindDirection, currentWindDirectionVoltage, insideTemperature, insideHumidity, AQI) VALUES(UTC_TIMESTAMP(), %.3f, %.3f, %.3f, "%s", %.3f, %.3f, %.3f, %i, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)' % (as3935LightningCount, as3935LastInterrupt, as3935LastDistance, as3935LastStatus, state.ScurrentWindSpeed, state.ScurrentWindGust, state.currentTotalRain,  state.currentInsideTemperature, state.currentBarometricPressure, state.currentAltitude,  state.currentSeaLevel,  state.currentOutsideTemperature, state.currentOutsideHumidity, state.ScurrentWindDirection, currentWindDirectionVoltage, state.currentInsideTemperature, state.currentInsideHumidity, state.Outdoor_AirQuality_Sensor_Value)
		print("query=%s" % query)

		cur.execute(query)


		# now check for TSL2591 Sensor
		if (config.TSL2591_Present):

			query = 'INSERT INTO Sunlight(TimeStamp, Visible, IR, UV, UVIndex) VALUES(UTC_TIMESTAMP(), %d, %d, %d, %.3f)' % (SunlightVisible, SunlightIR, SunlightUV, SunlightUVIndex)
			print("query=%s" % query)
			cur.execute(query)

	
		# now check for Sunlight Sensor
		if (config.Sunlight_Present):

			query = 'INSERT INTO Sunlight(TimeStamp, Visible, IR, UV, UVIndex) VALUES(UTC_TIMESTAMP(), %d, %d, %d, %.3f)' % (SunlightVisible, SunlightIR, SunlightUV, SunlightUVIndex)
			print("query=%s" % query)
			cur.execute(query)

	
		con.commit()
		
	except mdb.Error, e:
  
    		print "Error %d: %s" % (e.args[0],e.args[1])
    		con.rollback()
    		#sys.exit(1)
    
	finally:    
       		cur.close() 
        	con.close()

		del cur
		del con





def writePowerRecord():

	# now we have the data, stuff it in the database

	try:
		print("trying database")
    		con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SkyWeather');

    		cur = con.cursor()
		print "before query"

                if (config.SolarMAX_Present == True):
		        query = 'INSERT INTO PowerSystem(TimeStamp, batteryVoltage, batteryCurrent, solarVoltage, solarCurrent, loadVoltage, loadCurrent, batteryPower, solarPower, loadPower, batteryCharge) VALUES (UTC_TIMESTAMP (), %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)' % (state.batteryVoltage, state.batteryCurrent, state.solarVoltage, state.solarCurrent, state.loadVoltage, state.loadCurrent, state.batteryPower, state.solarPower, state.loadPower, state.batteryCharge) 
                else:
		
                  if (config.SunAirPlus_Present == False):
                    if (config.WXLink_Present):
		        query = 'INSERT INTO PowerSystem(TimeStamp, batteryVoltage, batteryCurrent, solarVoltage, solarCurrent, loadVoltage, loadCurrent, batteryPower, solarPower, loadPower, batteryCharge) VALUES (UTC_TIMESTAMP (), %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)' % (state.WXbatteryVoltage, state.WXbatteryCurrent, state.WXsolarVoltage, state.WXsolarCurrent, state.WXloadVoltage, state.WXloadCurrent, state.WXbatteryPower, state.WXsolarPower, state.WXloadPower, state.WXbatteryCharge) 
	            else:
		        query = 'INSERT INTO PowerSystem(TimeStamp, batteryVoltage, batteryCurrent, solarVoltage, solarCurrent, loadVoltage, loadCurrent, batteryPower, solarPower, loadPower, batteryCharge) VALUES (UTC_TIMESTAMP (), %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)' % (batteryVoltage, batteryCurrent, solarVoltage, solarCurrent, loadVoltage, loadCurrent, batteryPower, solarPower, loadPower, batteryCharge) 
                  else:
		    query = 'INSERT INTO PowerSystem(TimeStamp, batteryVoltage, batteryCurrent, solarVoltage, solarCurrent, loadVoltage, loadCurrent, batteryPower, solarPower, loadPower, batteryCharge) VALUES (UTC_TIMESTAMP (), %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f)' % (batteryVoltage, batteryCurrent, solarVoltage, solarCurrent, loadVoltage, loadCurrent, batteryPower, solarPower, loadPower, batteryCharge) 
                
		print("query=%s" % query)
                

		cur.execute(query)
	
		con.commit()
		
	except mdb.Error, e:
  
    		print "Error %d: %s" % (e.args[0],e.args[1])
    		con.rollback()
    		#sys.exit(1)
    
	finally:    
       		cur.close() 
        	con.close()

		del cur
		del con





def patTheDog():


	# pat the dog
	print "------Patting The Dog------- "
        GPIO.setup(config.WATCHDOGTRIGGER, GPIO.OUT)
        GPIO.output(config.WATCHDOGTRIGGER, False)
        time.sleep(0.2)
        GPIO.output(config.WATCHDOGTRIGGER, True)
        GPIO.setup(config.WATCHDOGTRIGGER, GPIO.IN)


	
def shutdownPi(why):

   pclogging.log(pclogging.INFO, __name__, "Pi Shutting Down: %s" % why)
   sendemail.sendEmail("test", "SkyWeather Shutting down:"+ why, "The SkyWeather Raspberry Pi shutting down.", config.notifyAddress,  config.fromAddress, "");
   sys.stdout.flush()
   time.sleep(10.0)

   os.system("sudo shutdown -h now")

def rebootPi(why):

   pclogging.log(pclogging.INFO, __name__, "Pi Rebooting: %s" % why)
   if (config.USEBLYNK):
     updateBlynk.blynkEventUpdate("Pi Rebooting: %s" % why)
     updateBlynk.blynkStatusTerminalUpdate("Pi Rebooting: %s" % why)
   pclogging.log(pclogging.INFO, __name__, "Pi Rebooting: %s" % why)
   os.system("sudo shutdown -r now")



import urllib2 


def checkInternetConnection():
    try:
        urllib2.urlopen("http://www.google.com").close()
    except urllib2.URLError:
        print "Internet Not Connected"
        time.sleep(1)
	return False
    else:
        print "Internet Connected"
	return True


WLAN_check_flg = 0

def WLAN_check():
        '''
        This function checks if the WLAN is still up by pinging the router.
        If there is no return, we'll reset the WLAN connection.
        If the resetting of the WLAN does not work, we need to reset the Pi.
        source http://www.raspberrypi.org/forums/viewtopic.php?t=54001&p=413095
        '''
	global WLAN_check_flg

        if (config.enable_WLAN_Detection == True):
          ping_ret = subprocess.call(['ping -c 2 -w 1 -q '+config.PingableRouterAddress+' |grep "1 received" > /dev/null 2> /dev/null'], shell=True)

	  print "checking WLAN:  ping_ret=%i WLAN_check_flg=%i" % (ping_ret, WLAN_check_flg)
	  if ping_ret:
            # we lost the WLAN connection.
            # did we try a recovery already?
            if (WLAN_check_flg>2):
                # we have a serious problem and need to reboot the Pi to recover the WLAN connection
		print "logger WLAN Down, Pi is forcing a reboot"
   		pclogging.log(pclogging.ERROR, __name__, "WLAN Down, Pi is forcing a reboot")
                WLAN_check_flg = 0 
		
		time.sleep(5)
		print "time to Reboot Pi from WLAN_check"
		rebootPi("WLAN Down reboot")
		#print "logger WLAN Down, Pi is forcing a Shutdown"
		#shutdownPi("WLAN Down halt") # halt pi and let the watchdog restart it
                #subprocess.call(['sudo shutdown -r now'], shell=True)
            else:
                # try to recover the connection by resetting the LAN
                #subprocess.call(['logger "WLAN is down, Pi is resetting WLAN connection"'], shell=True)
		print "WLAN Down, Pi is trying resetting WLAN connection"
   		pclogging.log(pclogging.WARNING, __name__, "WLAN Down, Pi is resetting WLAN connection" )
                WLAN_check_flg = WLAN_check_flg + 1 # try to recover
                subprocess.call(['sudo /sbin/ifdown wlan0 && sleep 10 && sudo /sbin/ifup --force wlan0'], shell=True)
          else:
            WLAN_check_flg = 0
	    print "WLAN is OK"

        else:    
	    # enable_WLAN_Detection is off
            WLAN_check_flg = 0
	    print "WLAN Detection is OFF"


#Rain calculations

rainArray = []
for i in range(20):
	rainArray.append(0)

lastRainReading = 0.0

def addRainToArray(plusRain):
	global rainArray
	del rainArray[0]
	rainArray.append(plusRain)
	#print "rainArray=", rainArray

def totalRainArray():
	global rainArray
	total = 0
	for i in range(20):
		total = total+rainArray[i]
	return total


# print out faults inside events
def ap_my_listener(event):
        if event.exception:
              print event.exception
              print event.traceback

# apscheduler events

def tick():
    print('Tick! The time is: %s' % datetime.now())


def killLogger():
    scheduler.shutdown()
    print "Scheduler Shutdown...."
    exit()

def updateRain():
	global lastRainReading, rain60Minutes
	addRainToArray(totalRain - lastRainReading)	
	rain60Minutes = totalRainArray()
	lastRainReading = totalRain

def statusRain():
        if (config.USEBLYNK):
            updateBlynk.blynkStatusTerminalUpdate("Rain in past 60 minutes=%0.2fmm"%rain60Minutes)

def statusAM2315():
        if (config.USEBLYNK):
            if (config.AM2315_Present):
                updateBlynk.blynkStatusTerminalUpdate("AM2315 ST: (g,br,bc,rt,pc) %s"% str(am2315.read_status_info()))
            if (config.SHT30_Present):
                updateBlynk.blynkStatusTerminalUpdate("SHT30 ST: (g,br,bc,rt,pc) %s"% str(sht30.read_status_info()))

def checkForShutdown():
	if (batteryVoltage < 3.5):
		print "--->>>>Time to Shutdown<<<<---"
                if (config.USEBLYNK):
                    updateBlynk.blynkStatusTerminalUpdate("Low Voltage Shutdown")
		shutdownPi("low voltage shutdown")


def barometricTrend():
    if (state.currentBarometricPressure >= state.pastBarometricReading):
        state.barometricTrend = True
    else:
        state.barometricTrend = False

    state.pastBarometricReading = state.currentBarometricPressure

def checkForButtons():
    reinitializeOLED = False
    if ((state.runOLED == False) and (config.OLED_Originally_Present == True)):
        reinitializeOLED = True

    if (config.USEBLYNK):
        updateBlynk.blynkStatusUpdate()

    if ((state.runOLED == True) and (reinitializeOLED == True)):
        I2C_Lock.acquire()
        initializeOLED()
        I2C_Lock.release()
        



print  ""
print "SkyWeather Weather Station Version "+config.SWVERSION+" - SwitchDoc Labs"
print ""
print ""
print "Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S")
print ""

###############
#  Turn Dust Sensor Off
################

GPIO.setup(config.DustSensorPowerPin, GPIO.OUT)
GPIO.output(config.DustSensorPowerPin, False)


# Initialize Variables
bmp180Temperature =  0
bmp180Pressure = 0 
bmp180Altitude = 0
bmp180SeaLevel = 0 
bmp180Humidity = 0


print "----------------------"
print returnStatusLine("I2C Mux - TCA9545",config.TCA9545_I2CMux_Present)
print returnStatusLine("BME680",config.BME680_Present)
print returnStatusLine("BMP280",config.BMP280_Present)
print returnStatusLine("SkyCam",config.Camera_Present)
print returnStatusLine("DS3231",config.DS3231_Present)
print returnStatusLine("HDC1080",config.HDC1080_Present)
print returnStatusLine("SHT30",config.SHT30_Present)
print returnStatusLine("AM2315",config.AM2315_Present)
print returnStatusLine("ADS1015",config.ADS1015_Present)
print returnStatusLine("ADS1115",config.ADS1115_Present)
print returnStatusLine("AS3935",config.AS3935_Present)
print returnStatusLine("OLED",config.OLED_Present)
print returnStatusLine("SunAirPlus/SunControl",config.SunAirPlus_Present)
print returnStatusLine("SolarMAX",config.SolarMAX_Present)
print returnStatusLine("SI1145 Sun Sensor",config.Sunlight_Present)
print returnStatusLine("TSL2591 Sun Sensor",config.TSL2591_Present)
print returnStatusLine("DustSensor",config.DustSensor_Present)
print returnStatusLine("WXLink",config.WXLink_Present)
print returnStatusLine("Dual SolarMAX/WXLink",config.Dual_MAX_WXLink)
print
print returnStatusLine("UseBlynk",config.USEBLYNK)
print returnStatusLine("UseMySQL",config.enable_MySQL_Logging)
print returnStatusLine("Check WLAN",config.enable_WLAN_Detection)
print returnStatusLine("WeatherUnderground",config.WeatherUnderground_Present)
print returnStatusLine("UseWeatherStem",config.USEWEATHERSTEM)
print "----------------------"

if (config.USEBLYNK):
     updateBlynk.blynkInit()




# initialize appropriate weather variables
currentWindDirection = 0
currentWindDirectionVoltage = 0.0
rain60Minutes = 0.0

#as3935Interrupt = False

pclogging.log(pclogging.INFO, __name__, "SkyWeather Startup Version"+config.SWVERSION )

if (config.USEBLYNK):
     updateBlynk.blynkEventUpdate("SW Startup Version "+config.SWVERSION)
     updateBlynk.blynkStatusTerminalUpdate("SW Startup Version "+config.SWVERSION) 

subjectText = "The "+ config.STATIONKEY + " SkyWeather Raspberry Pi has #rebooted."
ipAddress = commands.getoutput('hostname -I')
bodyText = "SkyWeather Version "+config.SWVERSION+ " Startup \n"+ipAddress+"\n"
if (config.SunAirPlus_Present):
	sampleSunAirPlus()
	bodyText = bodyText + "\n" + "BV=%0.2fV/BC=%0.2fmA/SV=%0.2fV/SC=%0.2fmA" % (batteryVoltage, batteryCurrent, solarVoltage, solarCurrent)

sendemail.sendEmail("test", bodyText, subjectText ,config.notifyAddress,  config.fromAddress, "");




# Initial Sample And Display
sampleAndDisplay()

# test SkyWeather

print ("taking SkyPicture")
if(config.Camera_Present):
    SkyCamera.takeSkyPicture()
    #print ("sending SkyCamera")
    #SkyCamera.sendSkyWeather()

# Set up scheduler

scheduler = BackgroundScheduler()

# for debugging
scheduler.add_listener(ap_my_listener, apscheduler.events.EVENT_JOB_ERROR)

##############
# setup tasks
##############

# prints out the date and time to console
scheduler.add_job(tick, 'interval', seconds=60)

# sample and Watchdog jobs

scheduler.add_job(sampleAndDisplay, 'interval', seconds=30)
scheduler.add_job(patTheDog, 'interval', seconds=10)   # reset the WatchDog Timer

# every minute, check for button changes
scheduler.add_job(checkForButtons, 'interval', seconds=10)   

if (config.runLEDs):
    # blink optional life light
    
    scheduler.add_job(pixelDriver.blinkLED, 'interval', seconds=31, args=[PixelLock,0,Color(0,0,255),1,0.250])

    # Status lights
    scheduler.add_job(pixelDriver.statusLEDs, 'interval', seconds=15, args=[PixelLock])

# every 5 minutes, push data to mysql and check for shutdown

if (config.WXLink_Present)or (config.SolarMAX_Present):
	scheduler.add_job(readLoRa.readRawWXLink, 'interval', seconds=15)


if (config.enable_MySQL_Logging == True):
	scheduler.add_job(writeWeatherRecord, 'interval', seconds=5*60)
	scheduler.add_job(writePowerRecord, 'interval', seconds=5*60)

scheduler.add_job(updateRain, 'interval', seconds=5*60)
scheduler.add_job(statusRain, 'interval', seconds=60*60)

if (config.SWDEBUG):
    scheduler.add_job(statusAM2315, 'interval', seconds=15*60)


scheduler.add_job(checkForShutdown, 'interval', seconds=5*60)

# every 15 minutes, build new graphs
scheduler.add_job(doAllGraphs.doAllGraphs, 'interval', seconds=15*60) 

# every 30 minutes, check wifi connections 
scheduler.add_job(WLAN_check, 'interval', seconds=30*60)

# every 5 days at 00:04, reboot
scheduler.add_job(rebootPi, 'cron', day='5-30/5', hour=0, minute=4, args=["5 day Reboot"]) 
	
#check for Barometric Trend (every 15 minutes)
scheduler.add_job(barometricTrend, 'interval', seconds=15*60)

if (config.DustSensor_Present):
    scheduler.add_job(DustSensor.read_AQI, 'interval', seconds=60*15)
    
# sky camera
if (config.Camera_Present):
    scheduler.add_job(SkyCamera.takeSkyPicture, 'interval', seconds=config.INTERVAL_CAM_PICS__SECONDS) 


# start scheduler
scheduler.start()
print "-----------------"
print "Scheduled Jobs"
print "-----------------"
scheduler.print_jobs()
print "-----------------"


if (config.SunAirPlus_Present == False):

        	batteryCurrent = 0.0
        	batteryVoltage = 4.00 
		batteryPower = batteryVoltage * (batteryCurrent/1000)


        	solarCurrent = 0.0 
        	solarVoltage = 0.0 
		solarPower = solarVoltage * (solarCurrent/1000)

        	loadCurrent = 0.0
        	loadVoltage = 0.0 
		loadPower = loadVoltage * (loadCurrent/1000)

		batteryCharge = 0 

if (config.WXLink_Present == False):

        	WXbatteryCurrent = 0.0
        	WXbatteryVoltage = 4.00 
		WXbatteryPower = WXbatteryVoltage * (WXbatteryCurrent/1000)


        	WXsolarCurrent = 0.0 
        	WXsolarVoltage = 0.0 
		WXsolarPower = WXsolarVoltage * (WXsolarCurrent/1000)

        	WXloadCurrent = 0.0
        	WXloadVoltage = 0.0 
		WXloadPower = WXloadVoltage * (WXloadCurrent/1000)

		WXbatteryCharge = 0 

#  Main Loop


while True:
	
	# process Interrupts from Lightning

	if (as3935Interrupt == True):
                print "AS3935 Interrupt"
                I2C_Lock.acquire()

		try:
			process_as3935_interrupt()

			
                except IOError as e:

                        print "I/O error({0}): {1}".format(e.errno, e.strerror)
			print "exception - as3935 I2C did not work"
                I2C_Lock.release()

        # 	if (config.TCA9545_I2CMux_Present):
        #         	tca9545.write_control_register(TCA9545_CONFIG_BUS0)
	

	time.sleep(1.0)

