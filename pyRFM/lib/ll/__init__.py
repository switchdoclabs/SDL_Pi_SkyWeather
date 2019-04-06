"""
	LinkLayer submodule
	
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2016-12-28"
__version__	= "0.1.0"
__license__ = "GPL"

class Prototype():
	conf=		None
	PL=			None
	
	def __init__(self,cfg,pl):
		self.conf=cfg
		self.PL=pl
		self.PL.setIRQH(self._handleIRQ)
		self.postInit()
		
		
	def _handleIRQ(self):
		pass

def get(conf,pl=None):
	"""
		get a new LinkLayer instance, depending on config
		
		if a PhysicalLayer is given, it's added to the LinkLayer
	"""
	if conf['type'] in ['rfm9x', 'rfm95','rfm96','rfm97','rfm98']:
		from .ll_rfm9x import LinkLayer
	else:
		print('unsupported type')
		return None
	
	return LinkLayer(conf,pl)
