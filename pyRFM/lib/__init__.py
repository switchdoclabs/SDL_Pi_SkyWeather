"""
	pyRFM module
"""
__author__	= """Alexander Krause <alexander.krause@ed-solutions.de>"""
__date__ 		= "2016-12-28"
__version__	= "0.1.0"
__license__ = "GPL"


def getLL(cfg):
	"""
		get a ready to use LinkLayer, depending on config
		
		see examples how the config should look
	"""
	if 'pl' in cfg:
		from .pl import get as getPL
		
		pl=getPL(cfg['pl'])
	else:
		pl=None
		
	if 'll' in cfg:
		from .ll import get as getLL
		ll=getLL(cfg['ll'],pl)
	else:
		ll=None
		
	return ll
