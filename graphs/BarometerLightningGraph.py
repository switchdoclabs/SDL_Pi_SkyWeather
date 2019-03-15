# BarometerLightningGraph 
# filename: BarometerLightningGraph.py
# Version 1.1 03/30/15 
#
# contains graphing code 
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


def  BarometerLightningGraph(source,days,delay):


	
	print("BarometerLightningGraph source:%s days:%s" % (source,days))
	print("sleeping seconds:", delay)
	time.sleep(delay)
	print("BarometerLightningGraph running now")

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

		query = "SELECT TimeStamp, bmp180SeaLevel, as3935LastInterrupt, as3935LastDistance FROM WeatherData where  now() - interval %i hour < TimeStamp" % (days*24)
		print "query=", query
		cursor.execute(query)
		result = cursor.fetchall()
		
		t = []
		s = []
		u = []
		v = []

		for record in result:
  			t.append(record[0])
  			s.append(record[1])
  			u.append(record[2])
  			v.append(record[3])
		
		
		fig = pyplot.figure()

                print ("count of t=",len(t))
		if (len(t) == 0):
			return	
		#dts = map(datetime.datetime.fromtimestamp, s)
		#fds = dates.date2num(t) # converted
		# matplotlib date format object
		hfmt = dates.DateFormatter('%m/%d-%H')

		
		ax = fig.add_subplot(111)
		for i in range(len(s)):
			s[i] = s[i] * 10
		
                #ax.vlines(fds, -200.0, 1000.0,colors='w')
                ax.xaxis.set_major_locator(dates.HourLocator(interval=6))
		ax.xaxis.set_major_formatter(hfmt)
		pylab.xticks(rotation='vertical')

		pyplot.subplots_adjust(bottom=.3)
		pylab.plot(t, s, color='b',label="Barometric Pressure (mb) ",linestyle="-",marker=".")
		pylab.xlabel("Hours")
		pylab.ylabel("millibars")
		pylab.legend(loc='upper left')
		pylab.axis([min(t), max(t), 900, 1100])
		ax2 = pylab.twinx()
		pylab.ylabel("Last Interrupt / Distance ")

		# scale array

		for i in range(len(v)):
			v[i] = v[i] * 10
		for i in range(len(u)):
			u[i] = u[i] * 10
		

		pylab.plot(t, u, color='y',label="as3935 Last Interrupt",linestyle="-",marker=".")
		pylab.plot(t, v, color='r',label="as3935 Last Distance",linestyle="-",marker=".")
		pylab.axis([min(t), max(t), 0, max(u)])
		pylab.legend(loc='lower left')
		pylab.figtext(.5, .05, ("Barometer and Lightning Statistics Last %i Days" % days),fontsize=18,ha='center')

		#pylab.grid(True)

		pyplot.setp( ax.xaxis.get_majorticklabels(), rotation=70)
		ax.xaxis.set_major_formatter(dates.DateFormatter('%m/%d-%H'))
		pyplot.show()
		try:
			pyplot.savefig("/home/pi/RasPiConnectServer/static/BarometerLightningGraph.png")	
		except:
			pyplot.savefig("/home/pi/SDL_Pi_GroveWeatherPi/static/BarometerLightningGraph.png")	

		
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
		del t, s, u, v 
		gc.collect()
		print("BarometerLightningGraph finished now")
