#!/usr/bin/env python

import AM2315
import time
import traceback



thsen = AM2315.AM2315(powerpin=6)


while (1):
    '''
    try:    
        outsideHumidity, outsideTemperature, crc_check =thsen.fast_read_humidity_temperature_crc()
        print "FROT=", outsideTemperature
        print "FROH=", outsideHumidity
        print "FROCRC=", crc_check 
    except:
        traceback.print_exc()
        print "bad AM2315 read"
    ''' 
    #print "T   ", thsen.read_temperature()
    #print "H   ", thsen.read_humidity()
    #print "H,T ", thsen.read_humidity_temperature()
    #print "H,T,C ", thsen.read_humidity_temperature_crc()
    h,t,c = thsen.read_humidity_temperature_crc()
    print "CRC=0x%02x" % c
   

    print "AM2315 Stats: (g,br,bc,rt,pc)", thsen.read_status_info()

    time.sleep(2.0)
