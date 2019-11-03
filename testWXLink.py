import readLoRa
import state
import sys
from datetime import datetime


# Check for user imports
try:
                import conflocal as config
except ImportError:
                import config

################
# WXLink Setup

#resetWXLink()
sys.path.append('./pyRFM')
import lib as pyrfm

import readLoRa

try:
        
	

    conf={
	'll':{
		'type':'rfm95'
	},
	'pl':{
		'type':	'serial_seed',
		'port':	'/dev/ttyS0'
	}
    }


    state.ll=pyrfm.getLL(conf)

    if state.ll.setOpModeSleep(True,True):
	state.ll.setFiFo()
	state.ll.setOpModeIdle()
        state.ll.setModemConfig('Bw31_25Cr48Sf512');
	#state.ll.setModemConfig('Bw125Cr45Sf128');
	#state.ll.setPreambleLength(8)
	state.ll.setFrequency(434.0)
	state.ll.setTxPower(13)
	
        print('HW-Version: ', state.ll.getVersion())
        config.WXLink_Present = True

except:
        config.WXLink_Present = False

state.block1 = ""
state.block2 = ""

# for this test, we configure both WXLink and SolarMAX to receive all the messages

config.SolarMAX_Present = True
config.Dual_MAX_WXLink = True



if (config.WXLink_Present):

    while True:
        readLoRa.readRawWXLink()
        if (len(state.block1) > 3):
            rawProtocolID = state.block1[2]

            print(">>>>>>>>>>>>protocolblock=",rawProtocolID)

        readLoRa.readWXLink(state.block1, state.block2, state.stringblock1, state.stringblock2, state.block1_orig, state.block2_orig)

        # OK, clear blocks - we have interpreted them
        state.block1 = []
        state.block2 = []
        state.stringblock1 = ""
        state.stringblock2 = ""
        state.block1_orig = []
        state.block2_orig = []

        print('Tick! The time is: %s' % datetime.now())
else:
    print("WXLink Not Found")
