
import requests
import time 
import picamera

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
    camera.rotation = 90
    camera.resolution = (1920, 1080)
    # Camera warm-up time


    camera.annotate_foreground = picamera.Color(y=0.2,u=0, v=0)
    camera.annotate_background = picamera.Color(y=0.8, u=0, v=0)
    val = time.strftime("SkyWeather: %Y-%m-%d %H:%M:%S")  
    camera.annotate_text = val
    time.sleep(2)

    camera.capture('static/skycamera.jpg')
    camera.close()

    sendSkyPictureToWeatherStem()


import base64

def sendSkyPictureToWeatherStem():

    # defining the api-endpoint  
    API_ENDPOINT = "https://api.weatherstem.com/api/util"
     
    # your API key here 
    API_KEY = "3gj8i0rm"
  

    with open("static/skycamera.jpg", "rb") as image_file:
       encoded_string = base64.b64encode(image_file.read())

    if (config.SWDEBUG):
        print ("--------------------")
        print ("SkyCam Picture Sending")
        print ("--------------------")

    # data to be sent to api 
    data = {'data': encoded_string,
                'api_key':API_KEY, 
                'method': 'social_sky_image_upload',
                'body': config.STATIONDESCRIPT,
                'city': config.STATIONLOCATIONCITY,
                'state':config.STATIONLOCATIONSTATE
                } 
                #'country':'United States',
                #'zipcode': '99037',
  
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, json = data) 
  
    # extracting response text  
    pastebin_url = r.text 
    if (config.SWDEBUG):
        print("The pastebin URL is:%s"%pastebin_url) 
