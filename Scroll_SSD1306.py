#
# Libraries to use the SDL_1306 as a scrollable device for WPA V3
#

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

OLEDLines = ["","","","","",""]
width = 128
height = 64 
top = 0
lineheight = 10
currentLine = 0
offset = 0

image = Image.new('1', (width, height))


draw = ImageDraw.Draw(image)
# Load default font.

font = ImageFont.load_default()


def addLineOLED(display, text):

	
	global currentLine, offset, OLEDLines
	# Write line of text.

	# Draw a black filled box to clear the line.
	draw.rectangle((0,lineheight*currentLine, 127, lineheight*(currentLine+1)-1), outline=0, fill=0)
	draw.text((0, lineheight*currentLine),    text,  font=font, fill=255)
	OLEDLines[currentLine] = text 

	if (currentLine == 5):
		for i in range(0,5):
			j = 5 - i -1
			draw.rectangle((0,lineheight*(j), 127, lineheight*(j+1)-1), outline=0, fill=0)
			draw.text((0, lineheight*(j)),    OLEDLines[j],  font=font, fill=255)


	if (currentLine < 5): 
		currentLine = currentLine + 1
	else:
		currentLine = 5
		# rewrite lines 
	 	for i in range(0,5):
			OLEDLines[i] = OLEDLines[i+1]	
		'''
		for i in range(0,1):
        		offset = (offset + 1) % 64
        		display.command(0x40 | offset)
        		time.sleep(0.01)

		'''

	display.image(image)
	display.display()


def addNumberedLineOLED(display, linenumber, text):

	# write one line of text at linenumber

	draw.rectangle((0,lineheight*currentLine, 127, lineheight*(currentLine+1)-1), outline=0, fill=0)
	draw.text((0, linenumber*lineheight),    text,  font=font, fill=255)

	display.image(image)
	display.display()

