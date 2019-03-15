# PowerVoltageGraph  
# filename: VoltageGraph.py
# Version 1.3 09/12/13
# Version 1.4 03/30/15
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

def  PowerVoltageGraph(source,days,delay):


	
	print("PowerVoltageGraph source:%s days:%s delay:%i" % (source,days,delay))
	print("sleeping :",delay)
	time.sleep(delay)
	print("PowerVoltageGraph running now")
	
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

		query = "SELECT TimeStamp, solarVoltage, batteryVoltage, loadVoltage FROM PowerSystem where  now() - interval %i hour < TimeStamp" % (days*24)
		cursor.execute(query)
		result = cursor.fetchall()

		t = []
		s = []
		u = []
		v = []
		#x = []
		
		for record in result:
  			t.append(record[0])
  			s.append(record[1])
  			u.append(record[2])
  			v.append(record[3])
  			#x.append(record[4])
		fig = pyplot.figure()

		print ("count of t=",len(t))
		#print (t)
		if (len(t) == 0):
			return
		#dts = map(datetime.datetime.fromtimestamp, t)
		#print dts
		#fds = dates.date2num(t) # converted
		# matplotlib date format object
		hfmt = dates.DateFormatter('%m/%d-%H')

		fig = pyplot.figure()
		fig.set_facecolor('white')
		ax = fig.add_subplot(111,axisbg = 'white')
		#ax.vlines(fds, -200.0, 1000.0,colors='w')

		ax.xaxis.set_major_locator(dates.HourLocator(interval=6))
		ax.xaxis.set_major_formatter(hfmt)
		ax.set_ylim(bottom = -200.0)
		pyplot.xticks(rotation='vertical')
		pyplot.subplots_adjust(bottom=.3)
		pylab.plot(t, s, color='b',label="Solar",linestyle="-",marker=".")
		pylab.plot(t, u, color='r',label="Battery",linestyle="-",marker=".")
		pylab.plot(t, v, color='g',label="Load",linestyle="-",marker=".")
		#pylab.plot(t, x, color='m',label="Power Eff",linestyle="-",marker=".")
		pylab.xlabel("Hours")
		pylab.ylabel("Voltage V")
		pylab.legend(loc='upper left')

		if (max(u) > max(s)):
			myMax = max(u)+ 100.0
		else:
			myMax = max(s)
		pylab.axis([min(t), max(t), min(u), myMax])
		pylab.figtext(.5, .05, ("GroveWeatherPi Power Voltage Last %i Days" % days),fontsize=18,ha='center')
		pyplot.setp( ax.xaxis.get_majorticklabels(), rotation=70)

		pylab.grid(True)

		pyplot.show()
		try:
			pyplot.savefig("/home/pi/RasPiConnectServer/static/PowerVoltageGraph.png",facecolor=fig.get_facecolor())	
		except:
			pyplot.savefig("/home/pi/SDL_Pi_GroveWeatherPi/static/PowerVoltageGraph.png",facecolor=fig.get_facecolor())	


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
		print("PowerVoltageGraph finished now")
