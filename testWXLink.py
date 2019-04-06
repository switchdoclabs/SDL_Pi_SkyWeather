import readLoRa
import state
import sys

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
        WXLink_Present = True

except:
        WXLink_Present = False

state.block1 = ""
state.block2 = ""

if (WXLink_Present):

    while True:
        readLoRa.readRawWXLink()

        readLoRa.readWXLink(state.block1, state.block2, state.stringblock1, state.stringblock2, state.block1_orig, state.block2_orig)

else:
    print("WXLink Not Found")
