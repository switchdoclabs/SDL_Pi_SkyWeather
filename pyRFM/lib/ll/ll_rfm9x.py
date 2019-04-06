"""
	RFM95 / 98 / 99 LinkLayer
	
	includes basic rx/tx stuff and init
	
	many parts have been translated from SeedStudios
	Arduino LoRa code:
	https://github.com/Seeed-Studio/Grove_LoRa_433MHz_and_915MHz_RF
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2016-12-28"
__version__	= "0.1.0"
__license__ = "GPL"


import time
import array

from . import Prototype

RFM_REG_FIFO                            = 0x00
RFM_REG_OP_MODE                         = 0x01
RFM_REG_RESERVED                        = 0x02
RFM_REG_RESERVED                        = 0x03
RFM_REG_RESERVED                        = 0x04
RFM_REG_RESERVED                        = 0x05
RFM_REG_FRF_MSB                         = 0x06
RFM_REG_FRF_MID                         = 0x07
RFM_REG_FRF_LSB                         = 0x08
RFM_REG_PA_CONFIG                       = 0x09
RFM_REG_PA_RAMP                         = 0x0a
RFM_REG_OCP                             = 0x0b
RFM_REG_LNA                             = 0x0c
RFM_REG_FIFO_ADDR_PTR                   = 0x0d
RFM_REG_FIFO_TX_BASE_ADDR               = 0x0e
RFM_REG_FIFO_RX_BASE_ADDR               = 0x0f
RFM_REG_FIFO_RX_CURRENT_ADDR            = 0x10
RFM_REG_IRQ_FLAGS_MASK                  = 0x11
RFM_REG_IRQ_FLAGS                       = 0x12
RFM_REG_RX_NB_BYTES                     = 0x13
RFM_REG_RX_HEADER_CNT_VALUE_MSB         = 0x14
RFM_REG_RX_HEADER_CNT_VALUE_LSB         = 0x15
RFM_REG_RX_PACKET_CNT_VALUE_MSB         = 0x16
RFM_REG_RX_PACKET_CNT_VALUE_LSB         = 0x17
RFM_REG_MODEM_STAT                      = 0x18
RFM_REG_PKT_SNR_VALUE                   = 0x19
RFM_REG_PKT_RSSI_VALUE                  = 0x1a
RFM_REG_RSSI_VALUE                      = 0x1b
RFM_REG_HOP_CHANNEL                     = 0x1c
RFM_REG_MODEM_CONFIG1                   = 0x1d
RFM_REG_MODEM_CONFIG2                   = 0x1e
RFM_REG_SYMB_TIMEOUT_LSB                = 0x1f
RFM_REG_PREAMBLE_MSB                    = 0x20
RFM_REG_PREAMBLE_LSB                    = 0x21
RFM_REG_PAYLOAD_LENGTH                  = 0x22
RFM_REG_MAX_PAYLOAD_LENGTH              = 0x23
RFM_REG_HOP_PERIOD                      = 0x24
RFM_REG_FIFO_RX_BYTE_ADDR               = 0x25
RFM_REG_MODEM_CONFIG3                   = 0x26

RFM_REG_DIO_MAPPING1                    = 0x40
RFM_REG_DIO_MAPPING2                    = 0x41
RFM_REG_VERSION                         = 0x42

RFM_REG_TCXO                            = 0x4b
RFM_REG_PA_DAC                          = 0x4d
RFM_REG_FORMER_TEMP                     = 0x5b
RFM_REG_AGC_REF                         = 0x61
RFM_REG_AGC_THRESH1                     = 0x62
RFM_REG_AGC_THRESH2                     = 0x63
RFM_REG_AGC_THRESH3                     = 0x64

# == RFM_REG_OP_MODE ==
RFM_MODE_LONG_RANGE                   = 0x80
RFM_MODE_ACCESS_SHARED_REG            = 0x40
RFM_MODE                              = 0x07
RFM_MODE_SLEEP                        = 0x00
RFM_MODE_STDBY                        = 0x01
RFM_MODE_FSTX                         = 0x02
RFM_MODE_TX                           = 0x03
RFM_MODE_FSRX                         = 0x04
RFM_MODE_RXCONTINUOUS                 = 0x05
RFM_MODE_RXSINGLE                     = 0x06
RFM_MODE_CAD                          = 0x07

# == RFM_REG_PA_CONFIG ==
RFM_PA_SELECT                         = 0x80
RFM_MAX_POWER                         = 0x70
RFM_OUTPUT_POWER                      = 0x0f

# == RFM_REG_PA_RAMP ==
RFM_LOW_PN_TX_PLL_OFF                 = 0x10
RFM_PA_RAMP                           = 0x0f
RFM_PA_RAMP_3_4MS                     = 0x00
RFM_PA_RAMP_2MS                       = 0x01
RFM_PA_RAMP_1MS                       = 0x02
RFM_PA_RAMP_500US                     = 0x03
RFM_PA_RAMP_250US                     = 0x0
RFM_PA_RAMP_125US                     = 0x05
RFM_PA_RAMP_100US                     = 0x06
RFM_PA_RAMP_62US                      = 0x07
RFM_PA_RAMP_50US                      = 0x08
RFM_PA_RAMP_40US                      = 0x09
RFM_PA_RAMP_31US                      = 0x0a
RFM_PA_RAMP_25US                      = 0x0b
RFM_PA_RAMP_20US                      = 0x0c
RFM_PA_RAMP_15US                      = 0x0d
RFM_PA_RAMP_12US                      = 0x0e
RFM_PA_RAMP_10US                      = 0x0f

# == RFM_REG_OCP ==
RFM_OCP_ON                            = 0x20
RFM_OCP_TRIM                          = 0x1f

# == RFM_REG_LNA ==
RFM_LNA_GAIN                          = 0xe0
RFM_LNA_BOOST                         = 0x03
RFM_LNA_BOOST_DEFAULT                 = 0x00
RFM_LNA_BOOST_150PC                   = 0x11

# == RFM_REG_IRQ_FLAGS ==
RFM_IF_RX_TIMEOUT                        = 0x80
RFM_IF_RX_DONE                           = 0x40
RFM_IF_PAYLOAD_CRC_ERROR                 = 0x20
RFM_IF_VALID_HEADER                      = 0x10
RFM_IF_TX_DONE                           = 0x08
RFM_IF_CAD_DONE                          = 0x04
RFM_IF_FHSS_CHANGE_CHANNEL               = 0x02
RFM_IF_CAD_DETECTED                      = 0x01

# == RFM_REG_MODEM_STAT ==
RFM_RX_CODING_RATE                    = 0xe0
RFM_MODEM_STATUS_CLEAR                = 0x10
RFM_MODEM_STATUS_HEADER_INFO_VALID    = 0x08
RFM_MODEM_STATUS_RX_ONGOING           = 0x04
RFM_MODEM_STATUS_SIGNAL_SYNCHRONIZED  = 0x02
RFM_MODEM_STATUS_SIGNAL_DETECTED      = 0x01

# == RFM_REG_HOP_CHANNEL ==
RFM_PLL_TIMEOUT                       = 0x80
RFM_RX_PAYLOAD_CRC_IS_ON              = 0x40
RFM_FHSS_PRESENT_CHANNEL              = 0x3f

# == RFM_REG_MODEM_CONFIG1 ==
RFM_BW                                = 0xc0
RFM_BW_125KHZ                         = 0x00
RFM_BW_250KHZ                         = 0x40
RFM_BW_500KHZ                         = 0x80
RFM_BW_RESERVED                       = 0xc0
RFM_CODING_RATE                       = 0x38
RFM_CODING_RATE_4_5                   = 0x00
RFM_CODING_RATE_4_6                   = 0x08
RFM_CODING_RATE_4_7                   = 0x10
RFM_CODING_RATE_4_8                   = 0x18
RFM_IMPLICIT_HEADER_MODE_ON           = 0x04
RFM_RX_PAYLOAD_CRC_ON                 = 0x02
RFM_LOW_DATA_RATE_OPTIMIZE            = 0x01

# == RFM_REG_MODEM_CONFIG2 ==
RFM_SPREADING_FACTOR                  = 0xf0
RFM_SPREADING_FACTOR_64CPS            = 0x60
RFM_SPREADING_FACTOR_128CPS           = 0x70
RFM_SPREADING_FACTOR_256CPS           = 0x80
RFM_SPREADING_FACTOR_512CPS           = 0x90
RFM_SPREADING_FACTOR_1024CPS          = 0xa0
RFM_SPREADING_FACTOR_2048CPS          = 0xb0
RFM_SPREADING_FACTOR_4096CPS          = 0xc0
RFM_TX_CONTINUOUS_MOE                 = 0x08
RFM_AGC_AUTO_ON                       = 0x04
RFM_SYM_TIMEOUT_MSB                   = 0x03

# == RFM_REG_PA_DAC ==
RFM_PA_DAC_DISABLE                    = 0x04
RFM_PA_DAC_ENABLE                     = 0x07

RFM_DEFAULT_MODEM_CFG={
	#										0x1d, 0x1e, 0x26
	#Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on. Default medium range
	'Bw125Cr45Sf128':		[0x72,   0x74,    0x00],
		
	#Bw = 500 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on. Fast+short range
	'Bw500Cr45Sf128':		[0x92,   0x74,    0x00],
	
	#Bw = 31.25 kHz, Cr = 4/8, Sf = 512chips/symbol, CRC on. Slow+long range
	'Bw31_25Cr48Sf512':	[0x48,   0x94,    0x00],
		
	#Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. Slow+long range
	'Bw125Cr48Sf4096':	[0x78,   0xc4,    0x00]
}

RFM_FXOSC = 32000000.0
#The Frequency Synthesizer step = RFM_FXOSC / 2^^19
RFM_FSTEP = (RFM_FXOSC / 524288)

RFM_HEADER_LEN		= 4
#Max number of octets the LORA Rx/Tx FIFO can hold
RFM_FIFO_SIZE			= 255

#This is the maximum number of bytes that can be carried by the LORA.
#We use some for headers, keeping fewer for RadioHead messages
RFM_MAX_PAYLOAD_LEN = RFM_FIFO_SIZE

class LinkLayer(Prototype):
	_RX_Buffer=	None
	_TX_id=			0
	
	State=			None
	Mode=				None

	def postInit(self):
		self.flush()
		self.State={
			'RX_ok':		0, 
			'RX_fail':	0,
			'TX_ok':		0,
			'RSSI':			None
		}
		
	def getVersion(self):
		return self.PL.readRegister(RFM_REG_VERSION)

	def getOpMode(self):
		return self.PL.readRegister(RFM_REG_OP_MODE)
		
	def setFiFo(self,tx=0,rx=0):
		self.PL.writeRegister(
			RFM_REG_FIFO_TX_BASE_ADDR,
			tx
		)
		self.PL.writeRegister(
			RFM_REG_FIFO_RX_BASE_ADDR,
			rx
		)

	
	def setOpMode(self,mode,check=False):
		"""
			enable LoRa Sleep mode
			@para check
				check for sleep mode active
		"""
		self.Mode=mode
		#print('Mode',mode)
		self.PL.writeRegister(
			RFM_REG_OP_MODE,
			mode
		)
		if check:
			#time.sleep(0.1)
			t_timeout=time.time()+0.2
			mode=mode
			while time.time()<t_timeout:
				cMode=self.getOpMode()
				#print(cMode)
				if cMode == mode:
					return True
				time.sleep(0.01)
				
			return False
		
		
	def setOpModeSleep(self,lora=False,check=False):
		if lora:
			return self.setOpMode(RFM_MODE_SLEEP|RFM_MODE_LONG_RANGE,check)
		else:
			return self.setOpMode(RFM_MODE_SLEEP,check)
	
	def setOpModeIdle(self,check=False):
		return self.setOpMode(RFM_MODE_STDBY,check)

	def setOpModeTx(self,check=False):
		#Interrupt on TxDone
		ret=self.setOpMode(RFM_MODE_TX,check)
		self.PL.writeRegister(RFM_REG_DIO_MAPPING1, 0x40)
		return ret

	def setOpModeRx(self,check=False):
		#Interrupt on RxDone
		ret=self.setOpMode(RFM_MODE_RXCONTINUOUS,check)
		self.PL.writeRegister(RFM_REG_DIO_MAPPING1, 0x00)
		return ret
	
	def setModemRegisters(self,reg_data):
		self.PL.writeRegister(RFM_REG_MODEM_CONFIG1, reg_data[0])
		self.PL.writeRegister(RFM_REG_MODEM_CONFIG2, reg_data[1])
		self.PL.writeRegister(RFM_REG_MODEM_CONFIG3, reg_data[2])
    
	def setModemConfig(self,data):
		if type(data)==str:
			self.setModemRegisters(RFM_DEFAULT_MODEM_CFG[data])
	
	def setPreambleLength(self,length):
		self.PL.writeRegister(RFM_REG_PREAMBLE_MSB, length >> 8);
		self.PL.writeRegister(RFM_REG_PREAMBLE_LSB, length & 0xff);

	def setFrequency(self,freq):
		#Frf = FRF / FSTEP
		frf = int( (freq * 1000000.0) / RFM_FSTEP )
		self.PL.writeRegister(RFM_REG_FRF_MSB, (frf >> 16) & 0xff)
		self.PL.writeRegister(RFM_REG_FRF_MID, (frf >> 8) & 0xff)
		self.PL.writeRegister(RFM_REG_FRF_LSB, frf & 0xff)

	def setTxPower(self,power,useRFO=False):
		#different behaviours depending if the module use PA_BOOST or the RFO pin
		#for the transmitter output
		if (useRFO):
			if (power > 14):
				power = 14
			elif (power < -1):
				power = -1
				
				self.PL.writeRegister(RFM_REG_PA_CONFIG, RFM_MAX_POWER | (power + 1))
		
		else:
			if (power > 23):
				power = 23
			elif (power < 5):
				power = 5

			#For RFM_PA_DAC_ENABLE, manual says '+20dBm on PA_BOOST when OutputPower=0xf'
			#RFM_PA_DAC_ENABLE actually adds about 3dBm to all power levels. We will us it
			#for 21 and 23dBm
			if (power > 20):
				self.PL.writeRegister(RFM_REG_PA_DAC, RFM_PA_DAC_ENABLE)
				power = power - 3
			else:
				self.PL.writeRegister(RFM_REG_PA_DAC, RFM_PA_DAC_DISABLE)
				
			# RFM95/96/97/98 does not have RFO pins connected to anything. Only PA_BOOST
			# pin is connected, so must use PA_BOOST
			# Pout = 2 + OutputPower.
			# The documentation is pretty confusing on this topic: PaSelect says the max power is 20dBm,
			# but OutputPower claims it would be 17dBm.
			# My measurements show 20dBm is correct
			self.PL.writeRegister(RFM_REG_PA_CONFIG, RFM_PA_SELECT | (power-5))
		
		
	def _handleIRQ(self):
		# Read the interrupt register
		irq_flags = self.PL.readRegister(RFM_REG_IRQ_FLAGS)
		#print('_handleIRQ',self.Mode,irq_flags)
		if (self.Mode & RFM_MODE_FSRX) and (irq_flags&(RFM_IF_RX_TIMEOUT|RFM_IF_PAYLOAD_CRC_ERROR)):
			self.State['RX_fail']=self.State['RX_fail']+1
		
		if (self.Mode & RFM_MODE_FSRX) and (irq_flags&RFM_IF_RX_DONE):
			#print('IRQ / rx')
			#Have received a packet
			length = self.PL.readRegister(RFM_REG_RX_NB_BYTES)

			#Reset the fifo read ptr to the beginning of the packet
			self.PL.writeRegister(
				RFM_REG_FIFO_ADDR_PTR,
				self.PL.readRegister(RFM_REG_FIFO_RX_CURRENT_ADDR)
			)
			buf=self.PL.readRegister(RFM_REG_FIFO,length)
			self._RX_Buffer=self._RX_Buffer+buf
			
			#print(length,self._RX_Buffer)
			#Clear all IRQ flags
			self.PL.writeRegister(RFM_REG_IRQ_FLAGS, 0xff)

			#Remember the RSSI of this packet
			#this is according to the doc, but is it really correct?
			#weakest receiveable signals are reported RSSI at about -66
			self.State['RSSI'] = self.PL.readRegister(RFM_REG_PKT_RSSI_VALUE) - 137

			#We have received a message.
			#if (self.validateRxBuffer()):
			#	self.setOpModeIdle()
			
		elif (self.Mode & RFM_MODE_FSRX) and (irq_flags & RFM_IF_CAD_DONE):
			print('IRQ / rx CAD done')
				
		elif (self.Mode & RFM_MODE_FSTX) and (irq_flags & RFM_IF_TX_DONE):
			#print('IRQ / tx done')
			self.State['TX_ok']=self.State['TX_ok']+1
			self.setOpModeIdle()
			
		#Clear all IRQ flags
		#print('clearing IRQ flags')
		self.PL.writeRegister(RFM_REG_IRQ_FLAGS, 0xff)
		if (self.Mode & RFM_MODE_FSRX):
			self.setOpModeRx()
    
	def waitPacketSent(self,timeout=1):
		t_timeouted=time.time()+timeout
		while time.time()<t_timeouted:
			self.PL.checkIRQ()
			if not (self.Mode&RFM_MODE_FSTX):
				return True
			time.sleep(0.01)
		return False
	
	def waitRX(self,timeout=None):
		self.setOpModeRx()
		if timeout==None:
			while True:
				self.PL.checkIRQ()
				if len(self._RX_Buffer):
					return True
		else:
			t_timeouted=time.time()+timeout
			while time.time()<t_timeouted:
				self.PL.checkIRQ()
				if len(self._RX_Buffer):
					return True
				time.sleep(0.01)
			
	
	def available(self):
		self.PL.checkIRQ()
		return len(self._RX_Buffer)
	
	def recv(self,length=None,timeout=None):
		if length==None:
			self.waitRX(timeout)
		elif timeout:
			t_timeouted=time.time()+timeout
			while time.time()<t_timeouted:
				if self.available()>=length:
					return self._RX_Buffer[0:length]
		else:
			while True:
				if self.available()>=length:
					return self._RX_Buffer[0:length]
		#timeout hit, return what we got
		ret=self._RX_Buffer
		self._RX_Buffer=[]
		return ret
	
	def flush(self):
		self._RX_Buffer=[]
	
	def sendStr(self,text):
		data=list(array.array('B',(text.encode('iso8859-1'))))
		return self.send(data)
		
		
	def send(self,data):
		#print('send',data)
		if self.waitPacketSent():
			self.setOpModeIdle()
			
			#Position at the beginning of the FIFO
			self.PL.writeRegister(RFM_REG_FIFO_ADDR_PTR, 0)
			
			#The headers
			#<to> <from> <id> <flags> 
			self.PL.writeRegister(RFM_REG_FIFO, [0,0,self._TX_id,0])
			#The message data
			length=len(data) + RFM_HEADER_LEN
			self.PL.writeRegister(RFM_REG_FIFO, data);
			self.PL.writeRegister(RFM_REG_PAYLOAD_LENGTH, length)

			#Start the transmitter
			self._TX_id=(self._TX_id+1)&0xff
			self.setOpModeTx()
			
			#when Tx is done, interruptHandler will fire and radio mode will return to STANDBY
			
			#write(RFM_REG_12_IRQ_FLAGS, 0xff); // Clear all IRQ flags
    