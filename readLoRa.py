#!/usb/bin/env python

import sys
import os
import time
import array
import state
import struct

import util

import crcpython2

import updateBlynk

try:
        import conflocal as config
except ImportError:
        import config


# change this if you have changed the SolarMAX protocol number 8 is for SolarMAX Lipo and 10 is for SolarMAX LeadAcid

SOLARMAXPROTOCOL = 8

if (config.SolarMAX_Type == "LEAD"):
    SOLARMAXPROTOCOL = 10

# read WXLink and return list to set variables
crcCalc = crcpython2.CRCCCITT(version='XModem')



def readWXLink(block1, block2, stringblock1, stringblock2, block1_orig, block2_orig):
     if (config.SWDEBUG):
        print "Starting readWXLink"
     #oldblock1 = block1
     #oldblock2 = block2
     try:
		if ((len(block1) > 0) and (len(block2) > 0)):
			# check crc for errors - don't update data if crc is bad
                        if (config.SWDEBUG):
                            print ("block1 length=", len(block1))	
                            print ("block2 length=", len(block2))	
			#get crc from data
			receivedCRC = struct.unpack('H', str(block2[29:31]))[0]
			#swap bytes for receivedCRC
			receivedCRC = (((receivedCRC)>>8) | ((receivedCRC&0xFF)<<8))&0xFFFF
                        if (config.SWDEBUG):
			    print "ReversedreceivedCRC= %x" % receivedCRC
			    print "length of stb1+sb2=", len(stringblock1+stringblock2)
                	    print ''.join('{:02x}'.format(ord(x)) for x in stringblock1)
                	    print ''.join('{:02x}'.format(ord(x)) for x in stringblock2)
			calculatedCRC = crcCalc.calculate(block1+block2[0:27])	
			
                        if (config.SWDEBUG):
			    print "calculatedCRC = %x " % calculatedCRC 

			# check for start bytes, if not present, then invalidate CRC

			if (block1[0] != 0xAB) or (block1[1] != 0x66):
				calculatedCRC = receivedCRC + 1

			if (receivedCRC == calculatedCRC):
                                if (config.SWDEBUG):
			        	print "Good CRC Recived"

                                # read protocol

                                protocol_byte = block1[2]
                                #protocol_byte = struct.unpack('B', str(block1[2:2]))[0]
                                protocol_ID = protocol_byte / 10
                                protocol_software_version = protocol_byte - protocol_ID*10
                                if (config.SWDEBUG):
                                        print("protocol_ID = ", protocol_ID)
                                        print("protocol_software_version = ", protocol_software_version)

                                # if protocol_ID == 3, then 
                                # use if:  SolarMAX_Present == False or Dual_MAX_WXLink == True
                                if ((protocol_ID == 3) and ((config.SolarMAX_Present == False) or (config.Dual_MAX_WXLink == True))):    # 3 is the WXLink Protocol

                                    print("protocol 3 - WXLink received")
                		    currentWindSpeed = struct.unpack('f', str(block1[9:13]))[0] 

                		    currentWindGust = 0.0   # not implemented in Solar WXLink version


                		    totalRain = struct.unpack('l', str(block1[17:21]))[0]
    	
                                    if (config.SWDEBUG):
                		        print("Rain Total=\t%0.2f in")%(totalRain/25.4)
                		        print("Wind Speed=\t%0.2f MPH")%(currentWindSpeed/1.6)
	    	
                		    currentWindDirection = struct.unpack('H', str(block1[7:9]))[0]
                                    if (config.SWDEBUG):
                		        print "Wind Direction=\t\t\t %i Degrees" % currentWindDirection
	    	
                		    # now do the AM2315 Temperature
                		    temperature = struct.unpack('f', str(block1[25:29]))[0]
                                    if (config.SWDEBUG):
                	                print "OTFloat=%x%x%x%x" %(block1[25], block1[26], block1[27], block1[28])
				    elements = [block1[29], block1[30], block1[31], block2[0]]
                		    outHByte = bytearray(elements)
                		    humidity = struct.unpack('f', str(outHByte))[0]
                                    if (config.SWDEBUG):
                		        print "AM2315 from WXLink temperature: %0.1fC" % temperature
                		        print "AM2315 from WXLink humidity: %0.1f%%" % humidity



                		    # now read the SunAirPlus Data from WXLink
	    	
                		    WXbatteryVoltage = struct.unpack('f', str(block2[1:5]))[0]
                		    WXbatteryCurrent = -struct.unpack('f', str(block2[5:9]))[0]
                		    WXloadCurrent = struct.unpack('f', str(block2[9:13]))[0]
                		    WXsolarPanelVoltage = struct.unpack('f', str(block2[13:17]))[0]
                		    WXsolarPanelCurrent = struct.unpack('f', str(block2[17:21]))[0]
    
		                    WXbatteryPower = WXbatteryVoltage * (WXbatteryCurrent/1000)
    
		                    WXsolarPower = WXsolarPanelVoltage * (WXsolarPanelCurrent/1000)
    
		                    WXloadPower = 5.0 * (WXloadCurrent/1000)

		                    WXbatteryCharge = util.returnPercentLeftInBattery(WXbatteryVoltage, 4.19)	

                		    state.WXbatteryVoltage = WXbatteryVoltage 
                		    state.WXbatteryCurrent = WXbatteryCurrent
                		    state.WXloadCurrent = WXloadCurrent
                		    state.WXsolarVoltage = WXsolarPanelVoltage
                		    state.WXsolarCurrent = WXsolarPanelCurrent
		                    state.WXbatteryPower = WXbatteryPower
		                    state.WXsolarPower = WXsolarPower
		                    state.WXloadPower = WXloadPower
		                    state.WXbatteryCharge = WXbatteryCharge

					
                		    auxA = struct.unpack('f', str(block2[21:25]))[0]
                                    # now set state variables

                                    if (config.SWDEBUG):
	
                		        print "WXLink batteryVoltage = %6.2f" % WXbatteryVoltage
                		        print "WXLink batteryCurrent = %6.2f" % WXbatteryCurrent
                		        print "WXLink loadCurrent = %6.2f" % WXloadCurrent
                		        print "WXLink solarPanelVoltage = %6.2f" % WXsolarPanelVoltage
                		        print "WXLink solarPanelCurrent = %6.2f" % WXsolarPanelCurrent
                		        print "WXLink auxA = %6.2f" % auxA
     	
                		    # message ID
                		    MessageID = struct.unpack('l', str(block2[25:29]))[0]
                		    print "WXLink Message ID %i" % MessageID
    
				    if (config.WXLink_LastMessageID != MessageID):
					    config.WXLink_Data_Fresh = True
					    config.WXLink_LastMessageID = MessageID
                                            if (config.SWDEBUG):
					        print "WXLink_Data_Fresh set to True"
                                #
                                # use protocol 8 if SolarMAX_Present == True 
                                #if (((protocol_ID == 8) or (protocol_ID == 10))and (config.SolarMAX_Present)):    # 8 is the WXLink Protocol
                                if ((protocol_ID == SOLARMAXPROTOCOL) and (config.SolarMAX_Present)):    # 8 is the WXLink Protocol
                                    ############################
                                    ############################
                                    ############################
                                    ############################
                                    #print("protocol 8 or 9 - SolarMAX received")
                                    print("protocol "+str(SOLARMAXPROTOCOL)+ " SolarMAX received")
                                    ############################
                                    ############################
                                    ############################
                                    ############################



                		    # now do the inside Temperature in the SolarMAX
                		    state.SolarMaxInsideTemperature = struct.unpack('f', str(block1[25:29]))[0]
                                    if (config.SWDEBUG):
                	                print "SMOTFloat=%x%x%x%x" %(block1[25], block1[26], block1[27], block1[28])
				    elements = [block1[29], block1[30], block1[31], block2[0]]
                		    outHByte = bytearray(elements)
                		    state.SolarMaxInsideHumidity = struct.unpack('f', str(outHByte))[0]
                                    if (config.SWDEBUG):
                		        print "ITemperature from SolarMAX temperature: %0.1fC" % state.SolarMaxInsideTemperature
                		        print "IHumidity from SolarMAX humidity: %0.1f%%" % state.SolarMaxInsideHumidity



                		    # now read the SolarMax Data from packet
                                    
	    	
                		    SolarMaxloadVoltage = struct.unpack('f', str(block1[21:25]))[0]

                		    SolarMaxbatteryVoltage = struct.unpack('f', str(block2[1:5]))[0]
                		    SolarMaxbatteryCurrent = -struct.unpack('f', str(block2[5:9]))[0]
                		    SolarMaxloadCurrent = struct.unpack('f', str(block2[9:13]))[0]
                		    SolarMaxsolarPanelVoltage = struct.unpack('f', str(block2[13:17]))[0]
                		    SolarMaxsolarPanelCurrent = -struct.unpack('f', str(block2[17:21]))[0]
    
		                    SolarMaxbatteryPower = SolarMaxbatteryVoltage * (SolarMaxbatteryCurrent/1000)
    
		                    SolarMaxsolarPower = SolarMaxsolarPanelVoltage * (SolarMaxsolarPanelCurrent/1000)
    
		                    SolarMaxloadPower = SolarMaxloadVoltage * (SolarMaxloadCurrent/1000)

		                    SolarMaxbatteryCharge = util.returnPercentLeftInBattery(SolarMaxbatteryVoltage, 4.19)	

                		    state.batteryVoltage = SolarMaxbatteryVoltage 
                		    state.batteryCurrent = SolarMaxbatteryCurrent
                		    state.loadCurrent = SolarMaxloadCurrent
                		    state.loadVoltage = SolarMaxloadVoltage
                		    state.solarVoltage = SolarMaxsolarPanelVoltage
                		    state.solarCurrent = SolarMaxsolarPanelCurrent
		                    state.batteryPower = SolarMaxbatteryPower
		                    state.solarPower = SolarMaxsolarPower
		                    state.loadPower = SolarMaxloadPower
		                    state.batteryCharge = SolarMaxbatteryCharge

					
                		    auxA = struct.unpack('f', str(block2[21:25]))[0]
                                    # now set state variables

	
                                    if (config.SWDEBUG):
                		        print "SolarMax batteryVoltage = %6.2f" % SolarMaxbatteryVoltage
                		        print "SolarMax batteryCurrent = %6.2f" % SolarMaxbatteryCurrent
                		        print "SolarMax loadVoltage = %6.2f" % SolarMaxloadVoltage
                		        print "SolarMax loadCurrent = %6.2f" % SolarMaxloadCurrent
                		        print "SolarMax solarPanelVoltage = %6.2f" % SolarMaxsolarPanelVoltage
                		        print "SolarMax solarPanelCurrent = %6.2f" % SolarMaxsolarPanelCurrent
                		        print "SolarMax auxA = %6.2f" % auxA
     	
                		    # message ID
                		    MessageID = struct.unpack('l', str(block2[25:29]))[0]
                		    print "SolarMax Message ID %i" % MessageID
                                    if (config.USEBLYNK):
                                        entry = time.strftime("%Y-%m-%d %H:%M:%S")+": %i \n" % (MessageID)
                                        updateBlynk.blynkSolarMAXLine(entry)
                                     
                                    if (config.SolarMAX_Present == True):
                                        if(config.SWDEBUG):
                                            if (config.USEBLYNK):
                                                updateBlynk.blynkStatusTerminalUpdate("SolarMAX ID# %d received:"%MessageID)
 

                                #if ((protocol_ID == 3) or (protocol_ID == 8) or (protocol_ID == 10)):
                                if ((protocol_ID == 3) or (protocol_ID == SOLARMAXPROTOCOL) ):
                                        pass
                                else:
                                    if (config.SWDEBUG):
				        print "unknown protocol received.  Protocol = ", protocol_ID
				    return []


			else:
				print "Bad CRC Received"
				return []

		else:
			return []
	
		# return list

                if (protocol_ID == 3):  # WXlink
		    returnList = []
                    returnList.append(protocol_ID)
		    returnList.append(block1_orig) 
		    returnList.append(block2_orig) 
		    returnList.append(currentWindSpeed) 
		    returnList.append(currentWindGust) 
		    returnList.append(totalRain) 
		    returnList.append(currentWindDirection) 
		    returnList.append(temperature) 
		    returnList.append(humidity) 
		    returnList.append(WXbatteryVoltage) 
		    returnList.append(WXbatteryCurrent) 
		    returnList.append(WXloadCurrent) 
		    returnList.append(WXsolarPanelVoltage) 
		    returnList.append(WXsolarPanelCurrent) 
		    returnList.append(auxA) 
		    returnList.append(MessageID) 
                else:
                    returnList = []   # protocol 8 - SolarMAX
                    returnList.append(protocol_ID)

		return returnList
     except Exception as e:
         print("LoRa Packet Decode Failure - probably short block receive")
         print("e=",e)
         return []

def readRawWXLink():
            
		
		if state.ll.waitRX(timeout=5):
                        if (config.SWDEBUG):
                            print("after WXLink waitRX")
			data=state.ll.recv()
			header=data[0:4]
			msg=data[4:]
			#print('header: ',header)
			#print('message:',array.array('B', msg).tostring())
                        #for i in range(0,len(data)): 
                        #    print('i={:d} {:d} 0x{:X}'.format( i,data[i],data[i]))
                       
                        if (config.SWDEBUG):
                	    print "-----------"
                        block1 = msg[0:32]
                        if (config.SWDEBUG):
			    print "block1=", block1
                        block2 = msg[32:65]
			state.block1_orig = block1
			state.block2_orig = block2
                        if (config.SWDEBUG):
			    print "block2=", block2
                        state.stringblock1 = ''.join(chr(e) for e in block1)
                        state.stringblock2 = ''.join(chr(e) for e in block2[0:27]) 

                        if (config.SWDEBUG):
                	    print "-----------"
                	    print "block 1"
                	    print ''.join('{:02x}'.format(x) for x in block1)
                	state.block1 = bytearray(block1)
                        if (config.SWDEBUG):
                	    print "block 2"
                	state.block2 = bytearray(block2)
                        if (config.SWDEBUG):
                	    print ''.join('{:02x}'.format(x) for x in block2)
                	    print "-----------"


                        
			
		            	
