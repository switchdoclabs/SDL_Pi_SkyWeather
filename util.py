
#utility programs
import state
import updateBlynk
import RPi.GPIO as GPIO

# Check for user imports
try:
                import conflocal as config
except ImportError:
                import config

GPIO.setmode(GPIO.BCM)

###############
# Turn OLED On and Off
###############

GROVEPOWERSAVEPIN = 12

def turnOLEDOn():
        GPIO.setup(GROVEPOWERSAVEPIN, GPIO.OUT)
        GPIO.output(GROVEPOWERSAVEPIN, True)
        if (config.USEBLYNK):
            updateBlynk.blynkStatusTerminalUpdate("OLED Turned On")
def turnOLEDOff():
        GPIO.setup(GROVEPOWERSAVEPIN, GPIO.OUT)
        GPIO.output(GROVEPOWERSAVEPIN, False)
        if (config.USEBLYNK):
            updateBlynk.blynkStatusTerminalUpdate("OLED Turned Off")


################
# Unit Conversion
################
# 

def returnTemperatureCF(temperature):
	if (state.EnglishMetric == True):
		# return Metric 
		return temperature
	else:
		return (9.0/5.0)*temperature + 32.0

def returnTemperatureCFUnit():
	if (state.EnglishMetric == True):
		# return Metric 
		return "C"
	else:
		return  "F"

def returnWindSpeedUnit():
	if (state.EnglishMetric == True):
		# return Metric 
		return "KPH"
	else:
		return  "MPH"

def returnWindSpeed(wind):
	if (state.EnglishMetric == True):
		# return Metric 
		return wind
	else:
		return wind/1.6


def returnWindDirection(windDirection):

    if (windDirection > 315.0+1.0):
        return "NNW"
    if (windDirection > 292.5+1.0):
        return "NW"
    if (windDirection > 270.0+1.0):
        return "WNW"
    if (windDirection > 247.5+1.0):
        return "W"
    if (windDirection > 225.0+1.0):
        return "WSW"
    if (windDirection > 202.5+1.0):
        return "SW"
    if (windDirection > 180.0+1.0):
        return "SSW"
    if (windDirection > 157.5+1.0):
        return "S"
    if (windDirection > 135.0+1.0):
        return "SSE"
    if (windDirection > 112.5+1.0):
        return "SE"
    if (windDirection > 90.0+1.0):
        return "ESE"
    if (windDirection > 67.5+1.0):
        return "E"
    if (windDirection > 45.0+1.0):
        return "ENE"
    if (windDirection > 22.5+1.0):
        return "NE"
    if (windDirection > 0.0+1.0):
        return "NNE"
    return "N"
