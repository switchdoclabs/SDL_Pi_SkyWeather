#!/usr/bin/env python

import SHT30
thsen = SHT30.SHT30(powerpin=6)

while (1):
	print "T   ", thsen.read_temperature()
	print "H   ", thsen.read_humidity()
	print "H,T ", thsen.read_humidity_temperature()
	print "H,T,C ", thsen.read_humidity_temperature_crc()
        h,t,cH,cT = thsen.read_humidity_temperature_crc()
        print "CRCH=0x%02x" % cH
        print "CRCT=0x%02x" % cT

