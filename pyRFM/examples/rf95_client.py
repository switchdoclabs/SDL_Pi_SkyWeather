#!/usb/bin/env python

"""
	send's a message and waits for a response
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2016-12-28"
__version__	= "0.1.0"
__license__ = "GPL"

import sys
import os
import time
import array

sys.path.append(
	os.path.join(
		os.path.dirname(__file__),
		'..'
	)
)
	
import lib as pyrfm

conf={
	'll':{
		'type':'rfm95'
	},
	'pl':{
		'type':	'serial_seed',
		'port':	'/dev/ttyS0'
	}
}
ll=pyrfm.getLL(conf)

print('HW-Version: ', ll.getVersion())
if ll.setOpModeSleep(True,True):
	ll.setFiFo()
	ll.setOpModeIdle()
        ll.setModemConfig('Bw31_25Cr48Sf512');
	#ll.setModemConfig('Bw125Cr45Sf128');
	#ll.setPreambleLength(8)
	ll.setFrequency(434.0)
	ll.setTxPower(13)
	
	while True:
		
		if ll.waitRX(timeout=5000):
                        print("after waitRX")
			data=ll.recv()
			header=data[0:4]
			msg=data[4:]
			print('header: ',header)
			print('message:',array.array('B', msg).tostring())
                        for i in range(0,len(data)): 
                            print('i={:d} {:d} 0x{:X}'.format( i,data[i],data[i]))
                        

		time.sleep(1)
			
			
