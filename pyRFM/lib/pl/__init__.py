"""
	PhysicalLayer submodule
	
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2016-12-28"
__version__	= "0.1.0"
__license__ = "GPL"

class Prototype():
	conf=		None
	
	def __init__(self,cfg):
		self.conf=cfg
	
	def setIRQH(self,callback):
		self._IRQH=callback
		
	def readRegister(self,addr):
		if self.PL:
			self.PL.flush()
			self.PL.write([addr,0])
			rx=self.PL.read(2)
			return rx[1]
	
	def writeRegister(self,addr,val):
		if self.PL:
			addr=addr | RFM_WRITE_REGISTER_MASK
			self.PL.flush()
			self.PL.write([addr,val])
			
			
def get(conf):
	"""
		get a new PhysicalLayer instance
	"""
	if conf['type']=='serial':
		from .pl_serial import PhysicalLayer
	elif conf['type']=='serial':
		from .pl_spi import PhysicalLayer
	elif conf['type']=='serial_seed':
		from .pl_serial_seed import PhysicalLayer
	else:
		print('unsupported type')
		return None
	
	return PhysicalLayer(conf)
