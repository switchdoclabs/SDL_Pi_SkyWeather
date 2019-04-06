#!/usb/bin/env python

"""
	simply try to get the hardware version
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2016-12-28"
__version__	= "0.1.0"
__license__ = "GPL"

import sys
import os

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

print(ll.getVersion())
