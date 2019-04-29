
import requests
import time 
import picamera
import state

# Check for user imports
try:
            import conflocal as config
except ImportError:
            import config

def takeSkyPicture():

    if (config.SWDEBUG):
        print ("--------------------")
        print ("SkyCam Picture Taken")
        print ("--------------------")
    camera = picamera.PiCamera()

    #camera.rotation = 180
    camera.rotation = 270
    camera.resolution = (1920, 1080)
    # Camera warm-up time


    camera.annotate_foreground = picamera.Color(y=0.2,u=0, v=0)
    camera.annotate_background = picamera.Color(y=0.8, u=0, v=0)
    val = time.strftime("SkyWeather: %Y-%m-%d %H:%M:%S")  
    camera.annotate_text = val
    time.sleep(2)

    camera.capture('static/skycamera.jpg')
    camera.close()

#    sendSkyPictureToWeatherStem()
    sendSkyWeather()


import base64


def sendSkyWeather():

    # defining the api-endpoint  
    API_ENDPOINT = "https://skyweather.weatherstem.com/"
     
    # your API key here 
    API_KEY = "3gj8i0rm"
  

    with open("static/skycamera.jpg", "rb") as image_file:
       encoded_string = base64.b64encode(image_file.read())

    if (config.SWDEBUG):
        print ("--------------------")
        print ("SkyCam Package Sending")
        print ("--------------------")

    if(state.barometricTrend == True):
        bptrendvalue = "Rising"
    else:
        bptrendvalue = "Falling"
   
    currentTime = time.time()


    data = {
                "SkyWeatherVersion": config.SWVERSION,
                "SkyWeatherHardware": config.STATIONHARDWARE,

	"device":{
                "key":  config.STATIONKEY,
                "MAC":config.STATIONMAC,
	},
	"utc":currentTime,
	"sensors":[


		{
			"name":"OutsideTemperature",
			"value": state.currentOutsideTemperature,
                        "units" : "C"

		},
		{
			"name":"OutsideHumidity",
			"value": state.currentOutsideHumidity,
                        "units" : "%"

		},
		{
			"name":"InsideTemperature",
			"value": state.currentInsideTemperature,
                        "units" : "C"
		},
		{
			"name":"InsideHumidity",
			"value": state.currentInsideHumidity,
                        "units" : "%"

		},
		{
			"name":"RainInLast60Minutes",
			"value": state.currentRain60Minutes,
                        "units" : "mm/h"
		},
		{
			"name":"VisibleSunlight",
			"value": state.currentSunlightVisible,
                        "units" : "lux"
		},
		{
			"name":"IRSunlight",
			"value": state.currentSunlightIR,
                        "units" : "lux"
		},
		{
			"name":"UVSunlightt",
			"value": state.currentSunlightUV,
                        "units" : "lux"

		},
		{
			"name":"WindSpeed",
			"value": state.ScurrentWindSpeed,
                        "units" : "kph"
		},
		{
			"name":"WindGust",
			"value": state.ScurrentWindGust,
                        "units" : "kph"
		},
		{
			"name":"WindDirection",
			"value": state.ScurrentWindDirection,
                        "units" : "degrees"
		},
		{
			"name":"totalRain",
			"value": state.currentTotalRain,
                        "units" : "mm"

		},
		{
			"name":"BarometricPressure",
			"value": state.currentBarometricPressure,
                        "units" : "hPa"

		},
		{
			"name":"Altitude",
			"value": state.currentAltitude,
                        "units" : "m"
		},
		{
			"name":"SeaLevelPressure",
			"value": state.currentSeaLevel,
                        "units" : "hPa"
		},
		{
			"name":"BarometricTrend",
			"value": bptrendvalue,
                        "units" : ""


		},
		{
			"name":"OutdoorAirQuality",
			"value": state.Outdoor_AirQuality_Sensor_Value,
                        "units" : "AQI"
		},
		{
			"name":"IndoorAirQuality",
			"value": state.Indoor_AirQuality_Sensor_Value,
                        "units" : "AQI"
		},
		{
			"name":"LastLightningDistance",
			"value": state.currentAs3935LastDistance,
                        "units" : "km"

		},
		{
			"name":"LastLightningTimeStamp",
			"value": state.currentAs3935LastLightningTimeStamp,
                        "units" : ""

		}
                ],
	"solarpower":[
		{
			"name":"BatteryVoltage",
			"value": state.batteryVoltage,
                        "units" : "V"


		},
		{
			"name":"BatteryCurrent",
			"value": state.batteryCurrent,
                        "units" : "ma"
		},
		{ 
                        "name":"SolarVoltage", 
                        "value": state.solarVoltage,
                        "units" : "V"
                },
		{
			"name":"SolarCurrent",
			"value": state.solarCurrent,
                        "units" : "ma"

		}, 
                {
			"name":"LoadVoltage",
			"value": state.loadVoltage,
                        "units" : "V"
		},
		{
			"name":"LoadCurrent",
			"value": state.loadCurrent,
                        "units" : "ma"
		},
		{
			"name":"BatteryPower",
			"value": state.batteryPower,
                        "units" : "W"
		},
		{
			"name":"SolarPower",
			"value": state.solarPower,
                        "units" : "W"
		},
		{
			"name":"LoadPower",
			"value": state.loadPower,
                        "units" : "W"
		},
		{
			"name":"BatteryCharge",
			"value": state.batteryCharge,
                        "units" : "%"

		},
		{
			"name":"WXBatteryVoltage",
			"value": state.WXbatteryVoltage,
                        "units" : "V"

		},
		{
			"name":"WXBatteryCurrent",
			"value": state.WXbatteryCurrent,
                        "units" : "ma"
		},
		{
			"name":"WXSolarVoltage",
			"value": state.WXsolarVoltage,
                        "units" : "V"
		},
		{
			"name":"WXSolarCurrent",
			"value": state.WXsolarCurrent,
                        "units" : "ma"
		},
		{
			"name":"WXLoadVoltage",
			"value": state.WXloadVoltage,
                        "units" : "V"
		},
		{
			"name":"WXLoadCurrent",
			"value": state.WXloadCurrent,
                        "units" : "ma"
		},
		{
			"name":"WXBatteryPOWER",
			"value": state.WXbatteryPower,
                        "units" : "W"
		},
		{
			"name":"WXSolarPower",
			"value": state.WXsolarPower,
                        "units" : "W"
		},
		{
			"name":"WXLoadPower",
			"value": state.WXloadPower,
                        "units" : "W"
		},
		{
			"name":"WXBatteryCharge",
			"value": state.WXbatteryCharge,
                        "units" : "%"


		}
		
	],
	"cameras":[
		{
			"name":"Sky Camera",
		}
		
	]
    }

    #"image": encoded_string

  
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, json = data) 
    print data 
    # extracting response text  
    pastebin_url = r.text 
    if (config.SWDEBUG):
        print("The pastebin URL is (r.text):%s"%pastebin_url) 



        
