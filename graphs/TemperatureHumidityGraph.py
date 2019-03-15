# TemperatureHumidityGraph 
# filename:TemperatureHumidityGraph.py
# Version 1.1 03/30/15
#
# contains event routines for data collection
#
#

import sys
import time
import RPi.GPIO as GPIO

import gc
import datetime

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

from matplotlib import pyplot
from matplotlib import dates

import pylab

import MySQLdb as mdb

# Check for user imports
try:
        import conflocal as config
except ImportError:
        import config



def  TemperatureHumidityGraph(source,days,delay):


	
	print("TemperatureHumidityGraph source:%s days:%s" % (source,days))
	print("sleeping seconds:", delay)
	time.sleep(delay)
	print("TemperatureHumidityGraph running now")
	

        # blink GPIO LED when it's run
        GPIO.setup(18, GPIO.OUT)
        GPIO.output(18, True)
        time.sleep(0.2)
        GPIO.output(18, False)

	# now we have get the data, stuff it in the graph 

	try:
		print("trying database")
    		db = mdb.connect('localhost', 'root', config.MySQL_Password, 'GroveWeatherPi');

    		cursor = db.cursor()

		query = "SELECT TimeStamp, bmp180Temperature,  outsideTemperature, outsideHumidity, insideHumidity FROM WeatherData where  now() - interval %i hour < TimeStamp" % (days*24)

		print "query=", query		
		cursor.execute(query)
		result = cursor.fetchall()

		t = []
		u = []
		v = []
	        x = []	
	        z = []	

		fig = pyplot.figure()



		for record in result:
  			t.append(record[0])
  			u.append(record[1])
  			v.append(record[2])
  			x.append(record[3])
  			z.append(record[4])

                print ("count of t=",len(t))
		if (len(t) == 0):
			return	

		#dts = map(datetime.datetime.fromtimestamp, s)
		#fds = dates.date2num(dts) # converted
		# matplotlib date format object
		hfmt = dates.DateFormatter('%m/%d-%H')

		
		ax = fig.add_subplot(111)
		ax.xaxis.set_major_locator(dates.HourLocator(interval=6))
		ax.xaxis.set_major_formatter(hfmt)
		pylab.xticks(rotation='vertical')

		pyplot.subplots_adjust(bottom=.3)
		pylab.plot(t, v, color='g',label="Outside Temp (C)",linestyle="-",marker=".")
		pylab.plot(t, u, color='r',label="Inside Temp (C)",linestyle="-",marker=".")
		pylab.xlabel("Hours")
		pylab.ylabel("degrees C")
		pylab.legend(loc='upper left')
		pylab.axis([min(t), max(t), 0, 40])
		ax2 = pylab.twinx()
		pylab.ylabel("% ")
		pylab.plot(t, x, color='y',label="Outside Hum %",linestyle="-",marker=".")
		pylab.plot(t, z, color='b',label="Inside Hum %",linestyle="-",marker=".")
		pylab.axis([min(t), max(t), 0, 100])
		pylab.legend(loc='lower left')
		pylab.figtext(.5, .05, ("Environmental Statistics Last %i Days" % days),fontsize=18,ha='center')

		#pylab.grid(True)

		pyplot.setp( ax.xaxis.get_majorticklabels(), rotation=70)
		ax.xaxis.set_major_formatter(dates.DateFormatter('%m/%d-%H'))
		pyplot.show()
		try:
			pyplot.savefig("/home/pi/RasPiConnectServer/static/TemperatureHumidityGraph.png")	
		except:
			pyplot.savefig("/home/pi/SDL_Pi_GroveWeatherPi/static/TemperatureHumidityGraph.png")	

		
	except mdb.Error, e:
  
    		print "Error %d: %s" % (e.args[0],e.args[1])
    
	finally:    

		cursor.close()       	 
        	db.close()

		del cursor
		del db

		fig.clf()
		pyplot.close()
		pylab.close()
		del t, u, v, x 
		gc.collect()
		print("TemperatureHumidityGraph finished now")
