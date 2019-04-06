"""
	serial access via SeedStudio's LoRa module:
	https://www.seeedstudio.com/Grove-LoRa-Radio-868MHz-p-2776.html
	
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2016-12-28"
__version__	= "0.1.0"
__license__ = "GPL"

from . import Prototype

import serial
import array

import sys

RFM_WRITE_REGISTER_MASK		= 1<<7


class PhysicalLayer(Prototype):
	isOpen=	False
	Con=		None
	
	def open(self):
		if not self.isOpen:
			self.Con=serial.Serial(
				port=self.conf['port'],
				baudrate=57600,
				timeout=0.5
			)
			self.isOpen=True
		else:
			pass
	
	def write(self,cmd,reg,length=None,data=None):
		if not self.isOpen:
			self.open()
		if self.isOpen:
			if data!=None:
				length=len(data)
				data=[reg,length]+data
			else:
				data=[reg,length]
				
			buff=array.array('B')
			buff.extend([cmd]+data)
			#print('write',cmd,data,buff)
			
			self.Con.write(buff)
	
	def read(self,length):
		#print('read',length)
		if not self.isOpen:
			self.open()
		if self.isOpen:
			data=self.Con.read(length)
			#print('ret',data)
			return list(array.array('B',(data)))
		
		return []

	def readRegister(self,addr,length=1):
		self.write(82,addr,length)
		rx=self.read(length)
		if length==1:
			return rx[0]
		else:
			return rx
		
	def writeRegister(self,addr,val):
		addr=addr | RFM_WRITE_REGISTER_MASK
		if type(val)==int:
			self.write(87,addr,None,[val])
		elif type(val)==list:
			self.write(87,addr,None,val)
		
	def checkIRQ(self):
		#print('checkIRQ')
		if not self.isOpen:
			self.open()
		if self.isOpen:
			if self.Con.inWaiting():
				data=self.read(self.Con.inWaiting())
				#print('...',data)
				if (data[0]==73) and self._IRQH:
					self._IRQH()
				
				
		