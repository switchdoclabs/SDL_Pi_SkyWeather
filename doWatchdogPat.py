# pats the WatchDog twice times and quits.  Allows for startup
# Check for user imports
try:
	import conflocal as config
except ImportError:
	import config

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
def patTheDog():


	# pat the dog
	print "------Pre Python Start Patting The Dog------- "
        GPIO.setup(config.WATCHDOGTRIGGER, GPIO.OUT)
        GPIO.output(config.WATCHDOGTRIGGER, False)
        time.sleep(0.2)
        GPIO.output(config.WATCHDOGTRIGGER, True)
        GPIO.setup(config.WATCHDOGTRIGGER, GPIO.IN)


# pat it twice 
while True:
    
    patTheDog()
    time.sleep(15)
    patTheDog()
