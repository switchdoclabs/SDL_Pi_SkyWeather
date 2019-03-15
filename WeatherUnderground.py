
#
# Send GroveWeatherPi Information to the WeatherUnderground
#
# SwitchDoc Labs September, 2016
# modifications November 2016 - Luksmann - changed to request library to improve reliablity
#
import sys
import requests
# import httplib

# Check for user imports
try:
        import conflocal as config
except ImportError:
        import config

def sendWeatherUndergroundData( as3935LightningCount, as3935, as3935LastInterrupt, as3935LastDistance, as3935LastStatus, currentWindSpeed, currentWindGust, totalRain, bmp180Temperature, bmp180Pressure, bmp180Altitude,  bmp180SeaLevel, outsideTemperature, outsideHumidity, crc_check, currentWindDirection, currentWindDirectionVoltage, HTUtemperature, HTUhumidity, rain60Minutes):

	# https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID=KCASANFR5&PASSWORD=XXXXXX&dateutc=2000-01-01+10%3A32%3A35&winddir=230&windspeedmph=12&windgustmph=12&tempf=70&rainin=0&baromin=29.1&dewptf=68.2&humidity=90&weather=&clouds=&softwaretype=vws%20versionxx&action=updateraw

	# build the URL
	myURL = "ID="+config.WeatherUnderground_StationID
	myURL += "&PASSWORD="+config.WeatherUnderground_StationKey
	myURL += "&dateutc=now"

	# now weather station variables

	myURL += "&winddir=%i" % currentWindDirection
	print "cws=|",currentWindSpeed

	myURL += "&windspeedmph=%0.2f" % (currentWindSpeed/1.6)
	myURL += "&windgustmph=%0.2f" % (currentWindGust/1.6)

	myURL += "&humidity=%i" % outsideHumidity
	myURL += "&tempf=%0.2f" % ((outsideTemperature*9.0/5.0)+32.0)

   	dewpoint =  outsideTemperature - ((100.0 - outsideHumidity) / 5.0);
	dewpointf = ((dewpoint*9.0/5.0)+32.0)
	myURL += "&dewptf=%0.2f" % dewpointf

	myURL += "&rainin=%0.2f" % ((rain60Minutes)/25.4)
	myURL += "&dailyrainin=%0.2f" % ((totalRain)/25.4)
	myURL += "&baromin=%0.2f" % ((bmp180SeaLevel) * 0.2953)

	myURL += "&indoortempf=%0.2f" % ((HTUtemperature*9.0/5.0)+32.0)
	myURL += "&indoorhumidity%0.2f=" % HTUhumidity

	myURL += "&software=GroveWeatherPi"



	print "myURL=", myURL
	#send it
	r = requests.get("https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php", params=myURL)

	print(r.url)
	print(r.text)
	print "GET sent"
