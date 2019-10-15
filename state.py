# 
# Contains updated State Variables for Blynk and Sections
#
#


# WeatherSTEM info

WeatherSTEMHash = ""

# Weather Variables

currentOutsideTemperature = 0.0
currentOutsideHumidity = 1

currentInsideTemperature = 0.0
currentInsideHumidity = 1

currentRain60Minutes = 0.0

currentSunlightVisible = 0
currentSunlightIR = 0
currentSunlightUV = 0
currentSunlightUVIndex  = 0

ScurrentWindSpeed = 0
ScurrentWindGust  = 0
ScurrentWindDirection  = 0.2
currentTotalRain  = 0

currentBarometricPressure = 0
currentAltitude = 0 
currentSeaLevel = 0
barometricTrend = True
pastBarometricReading = 0

Indoor_AirQuality_Sensor_Value = 0
Outdoor_AirQuality_Sensor_Value = 0
Hour24_Outdoor_AirQuality_Sensor_Value = 0




# Lightning Values

currentAs3935Interrupt = 0

currentAs3935LastInterrupt = 0
currentAs3935LastDistance = 0
currentAs3935LastStatus = 0

currentAs3935LastLightningTimeStamp = 0

# Button Variables

runRainbow = False
flashStrip = False
runOLED = True

# status Values

Last_Event = "My Last Event"
EnglishMetric = 0


# Solar Values


batteryVoltage = 0
batteryCurrent = 0
solarVoltage = 0
solarCurrent = 0
loadVoltage = 0
loadCurrent = 0
batteryPower = 0
solarPower = 0
loadPower = 0
batteryCharge = 0
SolarMAXLastReceived = "None"

# WXLink Values
WXbatteryVoltage = 0
WXbatteryCurrent = 0
WXsolarVoltage = 0
WXsolarCurrent = 0
WXloadVoltage = 5.0
WXloadCurrent = 0
WXbatteryPower = 0
WXsolarPower = 0
WXloadPower = 0
WXbatteryCharge = 0

# Fan State

fanState = False

# WXLink Blocks
block1 = ""
block2 = ""
stringblock1 = ""
stringblock2 = ""
block1_orig = ""
block2_orig = ""

ll = None

def printState():

    print "-------------"
    print "Current State"
    print "-------------"
    print"currentOutsideTemperature = ",currentOutsideTemperature 
    print"currentOutsideHumidity = ", currentOutsideHumidity 

    print"currentInsideTemperature = ",currentInsideTemperature
    print"currentInsideHumidity = ",  currentInsideHumidity 

    print"currentRain60Minutes = ",  currentRain60Minutes 

    print"currentSunlightVisible = ",  currentSunlightVisible 
    print"currentSunlightIR = ", currentSunlightIR 
    print"currentSunlightUV = ",  currentSunlightUV 
    print"currentSunlightUVIndex  = ", currentSunlightUVIndex  

    print"ScurrentWindSpeed = ", ScurrentWindSpeed
    print"ScurrentWindGust  = ",  ScurrentWindGust 
    print"ScurrentWindDirection  = ",  ScurrentWindDirection 
    print"currentTotalRain  = ", currentTotalRain  

    print "currentBarometricPressure = ", currentBarometricPressure 
    print "currentAltitude = ", currentAltitude 
    print "currentSeaLevel = ", currentSeaLevel 
    print "barometricTrend =",barometricTrend 
    print "pastBarometricReading = ", pastBarometricReading 

    print "Outdoor_AirQuality_Sensor_Value = ",  Outdoor_AirQuality_Sensor_Value 
    print "Hour24_Outdoor_AirQuality_Sensor_Value = ",  Hour24_Outdoor_AirQuality_Sensor_Value 
    print "Indoor_AirQuality_Sensor_Value = ",  Indoor_AirQuality_Sensor_Value 

    print "-------------"


    print "currentAs3935Interrupt = ", currentAs3935Interrupt 

    print "currentAs3935LastInterrupt = ", currentAs3935LastInterrupt 
    print "currentAs3935LastDistance = ",  currentAs3935LastDistance 
    print "currentAs3935LastStatus = ", currentAs3935LastStatus 
    
    print "currentAs3935LastLightningTimeStamp = ", currentAs3935LastLightningTimeStamp 


    
    print "-------------"


    print "runRainbow = ", runRainbow 
    print "flashStrip = ", flashStrip 
    print "runOLED =", runOLED 
    print "-------------"



    print "Last_Event = ", Last_Event 
    print "EnglishMetric = ", EnglishMetric 
    
    
    print "-------------"

    print "batteryVoltage", batteryVoltage 
    print "batteryCurrent", batteryCurrent
    print "solarVoltage", solarVoltage 
    print "solarCurrent", solarCurrent
    print "loadVoltage", loadVoltage
    print "loadCurrent", loadCurrent
    print "batteryPower", batteryPower
    print "solarPower", solarPower
    print "loadPower", loadPower
    print "batteryCharge", batteryCharge

    print "SolarMAX Last Received", SolarMAXLastReceived
    print "-------------"

    print "-------------"

    print "WXbatteryVoltage", WXbatteryVoltage 
    print "WXbatteryCurrent", WXbatteryCurrent
    print "WXsolarVoltage", WXsolarVoltage 
    print "WXsolarCurrent", WXsolarCurrent
    print "WXloadVoltage", WXloadVoltage
    print "WXloadCurrent", WXloadCurrent
    print "WXbatteryPower", WXbatteryPower
    print "WXsolarPower", WXsolarPower
    print "WXloadPower", WXloadPower
    print "WXbatteryCharge", WXbatteryCharge

    print "-------------"
    print "fanState = ", fanState
    print "-------------"
    print "WXLink Blocks"
    print "Block1 Length= ", len(block1)
    print "Block2 Length= ", len(block2)

