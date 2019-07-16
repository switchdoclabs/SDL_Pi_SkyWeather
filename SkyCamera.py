
import requests
import time 
import picamera
import state
import cv2
import traceback
import threading
import os
import sys

import util
import hashlib

import io
import logging
import SocketServer

import numpy as np
import datetime as dt

from threading import Condition
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

from PIL import ImageFont, ImageDraw, Image

import traceback
import StringIO

# Check for user imports
try:
            import conflocal as config
except ImportError:
            import config

def SkyWeatherKeyGeneration(userKey):

    catkey = "AZWqNqDMhvK8Lhbb2jtk1bucj0s2lqZ6" +userKey

    md5result = hashlib.md5(catkey)
    #print ("hashkey =", md5result.hexdigest())
    return md5result.hexdigest()


class SkyStreamClass():

    def mjpegStream(self):
        if (config.SWDEBUG):
            print ("--------------------")
            print ("SkyStream: mjpegStream Started ")
            print ("--------------------")




        PAGE="""\
        <html>
        <head>
        <title>SkyWeather MJPEG streaming demo</title>
        </head>
        <body>
        <h1>SkyWeather MJPEG Streaming Demo</h1>
        <img src="stream.mjpg" width="1296" height="730" />
        </body>
        </html>
        """

        class StreamingOutput(object):
            def __init__(self):
                self.frame = None
                self.buffer = io.BytesIO()
                self.condition = Condition()

            def write(self, buf):
                if buf.startswith(b'\xff\xd8'):
                    # New frame, copy the existing buffer's content and notify all
                    # clients it's available
                    self.buffer.truncate()
                    with self.condition:
                        self.frame = self.buffer.getvalue()
                        self.condition.notify_all()
                    self.buffer.seek(0)
                return self.buffer.write(buf)

        class StreamingHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(301)
                    self.send_header('Location', '/index.html')
                    self.end_headers()
                elif self.path == '/index.html':
                    content = PAGE.encode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Content-Length', len(content))
                    self.end_headers()
                    self.wfile.write(content)
                elif self.path == '/stream.mjpg':
                    self.send_response(200)
                    self.send_header('Age', 0)
                    self.send_header('Cache-Control', 'no-cache, private')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
                    self.end_headers()
                    try:
                        while True:
                            with output.condition:
                                output.condition.wait()
                                frame = output.frame
                                # now add timestamp to jpeg
                                # Convert to PIL Image
                                cv2.CV_LOAD_IMAGE_COLOR = 1 # set flag to 1 to give colour image
                                npframe = np.fromstring(frame, dtype=np.uint8)
                                pil_frame = cv2.imdecode(npframe,cv2.CV_LOAD_IMAGE_COLOR)
                                #pil_frame = cv2.imdecode(frame,-1)
                                cv2_im_rgb = cv2.cvtColor(pil_frame, cv2.COLOR_BGR2RGB)
                                pil_im = Image.fromarray(cv2_im_rgb)
        
                                draw = ImageDraw.Draw(pil_im)
        
                                # Choose a font
                                font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 25)

                                # set up units
                                #wind
                                val = util.returnWindSpeed(state.ScurrentWindSpeed)
                                WindStval = "{0:0.1f}".format(val) + util.returnWindSpeedUnit()
                                val = util.returnWindSpeed(state.ScurrentWindGust)
                                WindGtval = "{0:0.1f}".format(val) + util.returnWindSpeedUnit()
                                val = util.returnTemperatureCF(state.currentOutsideTemperature)
                                OTtval = "{0:0.1f} ".format(val) + util.returnTemperatureCFUnit()

                                myText = "SkyWeather   %s Wind Speed: %s Wind Gust:  %s Temp: %s " % (dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),WindStval, WindGtval, OTtval)
        
                                # Draw the text
                                color = 'rgb(255,255,255)'
                                #draw.text((0, 0), myText,fill = color, font=font)
        
                                # get text size
                                text_size = font.getsize(myText)
        
                                # set button size + 10px margins
                                button_size = (text_size[0]+20, text_size[1]+10)
        
                                # create image with correct size and black background
                                button_img = Image.new('RGBA', button_size, "black")
                             
                                #button_img.putalpha(128)
                                # put text on button with 10px margins
                                button_draw = ImageDraw.Draw(button_img)
                                button_draw.text((10, 5), myText, fill = color, font=font)
        
                                # put button on source image in position (0, 0)
        
                                pil_im.paste(button_img, (0, 0))
                                bg_w, bg_h = pil_im.size 
                                # WeatherSTEM logo in lower left
                                size = 64
                                WSLimg = Image.open("static/WeatherSTEMLogoSkyBackground.png")
                                WSLimg.thumbnail((size,size),Image.ANTIALIAS)
                                pil_im.paste(WSLimg, (0, bg_h-size))
        
                                # SkyWeather log in lower right
                                SWLimg = Image.open("static/SkyWeatherLogoSymbol.png")
                                SWLimg.thumbnail((size,size),Image.ANTIALIAS)
                                pil_im.paste(SWLimg, (bg_w-size, bg_h-size))

                                # Save the image
                                buf= StringIO.StringIO()
                                pil_im.save(buf, format= 'JPEG')
                                frame = buf.getvalue()
                            self.wfile.write(b'--FRAME\r\n')
                            self.send_header('Content-Type', 'image/jpeg')
                            self.send_header('Content-Length', len(frame))
                            self.end_headers()
                            self.wfile.write(frame)
                            self.wfile.write(b'\r\n')
                    except Exception as e:
                        logging.warning(
                            'Removed streaming client %s: %s',
                            self.client_address, str(e))
               
                else:
                    self.send_error(404)
                    self.end_headers()
            # removes the socket error
            '''
            def handle(self):
                try:
                    BaseHTTPServer.BaseHTTPRequestHandler.handle(self)
                except:
                    pass
            '''

        class StreamingServer(SocketServer.ThreadingMixIn, HTTPServer):
            allow_reuse_address = True
            daemon_threads = True
        
        
        # remove stdout prints from disconnects

        #with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        with picamera.PiCamera(resolution='1296x730', framerate=24) as camera:
                output = StreamingOutput()
                #camera.rotation = 180
                camera.rotation = 270
                camera.start_recording(output, format='mjpeg')
                try:
                    address = ('', 443)
                    server = StreamingServer(address, StreamingHandler)
                    server.serve_forever()

                finally:
                    camera.stop_recording()
        
        if (config.SWDEBUG):
            print ("--------------------")
            print ("SkyStream: mjpegStream Ended ")
            print ("--------------------")
        


    def runAutossh(self):
        if (config.SWDEBUG):
            print ("--------------------")
            print ("SkyStream: Autossh Started ")
            print ("--------------------")
     
            AutoCommand = "sudo /usr/bin/autossh -i /home/pi/.ssh/id_rsa -M 0 -o 'ExitOnForwardFailure yes' -o 'ServerAliveInterval 30' -o 'ServerAliveCountMax 3' -N -R octanemaster.ucompass.com:11000:127.0.0.1:443 skyweather@octanemaster.ucompass.com"

            os.system(AutoCommand) 



        if (config.SWDEBUG):
            print ("--------------------")
            print ("SkyStream: Autossh Ended  ")
            print ("--------------------")
        


def startSkyStream():

    if (config.SWDEBUG):
        print ("--------------------")
        print ("SkyStream Started ")
        print ("--------------------")

    # start two threads.  One for autossh and one for the stream mjpeg itself
    
    try:
        SkyStream = SkyStreamClass()

        threadAuto = threading.Thread(target = SkyStream.runAutossh)
        threadStream = threading.Thread(target = SkyStream.mjpegStream)
       
        threadAuto.start()

        time.sleep(2)
        threadStream.start()

    except:

        if (config.SWDEBUG):
            traceback.print_exc()
            print ("--------------------")
            print ("SkyStream Failed ")
            print ("--------------------")



def takeSkyStreamPicture():

    if (config.SWDEBUG):
        print ("--------------------")
        print ("SkyCam Stream Picture Taken")
        print ("--------------------")

    try:
        if (config.SWDEBUG):
            print "SkyStream: starting grab"
        URL ='http://localhost:'+str(config.STREAMLOCALPORT)+'/stream.mjpg'
        if (config.SWDEBUG):
            print "SkyStream: grab URL=", URL
        cap = cv2.VideoCapture(URL)

        ret, frame = cap.read()
        if (config.SWDEBUG):
            print "SkyStream: found frame"
        #cv2.imshow('Video', frame)
        cv2.imwrite("static/skycamera.jpg",frame)
        if (config.SWDEBUG):
            print "SkyStream: after release"
        cap.release()
        val = time.strftime("SkyWeather: %Y-%m-%d %H:%M:%S")  
        #camera.capture('static/skycamera.jpg')
    except:
            if (config.SWDEBUG):
                traceback.print_exc()
                print ("--------------------")
                print ("SkyCam Stream Picture Failed")
                print ("--------------------")


    finally:
        pass


    if (config.USEWEATHERSTEM == True):
        sendSkyWeather()



def takeSkyPicture():

    if (config.SWDEBUG):
        print ("--------------------")
        print ("SkyCam Picture Taken")
        print ("--------------------")
    camera = picamera.PiCamera()

    try:
        camera.rotation = 180
        #camera.rotation = 270
        camera.resolution = (1920, 1080)
        # Camera warm-up time


        camera.annotate_foreground = picamera.Color(y=0.2,u=0, v=0)
        camera.annotate_background = picamera.Color(y=0.8, u=0, v=0)
        val = time.strftime("SkyWeather: %Y-%m-%d %H:%M:%S")  
        camera.annotate_text = val
        time.sleep(2)

        camera.capture('static/skycamera.jpg')
    except:
            if (config.SWDEBUG):
                print ("--------------------")
                print ("SkyCam Picture Failed")
                print ("--------------------")


    finally:
        try:
            camera.close()
        except:
            if (config.SWDEBUG):
                print ("--------------------")
                print ("SkyCam Close Failed ")
                print ("--------------------")


    if (config.USEWEATHERSTEM == True):
        sendSkyWeather()


import base64


def sendSkyWeather():

    # defining the api-endpoint  
    API_ENDPOINT = "https://skyweather.weatherstem.com/"
     
  

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
                "api_key": state.WeatherSTEMHash,

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
                        "image": encoded_string
		}
		
	]
    }


  
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, json = data) 
    #print data 
    # extracting response text  
    pastebin_url = r.text 
    if (config.SWDEBUG):
        print("The pastebin URL is (r.text):%s"%pastebin_url) 



        
