SwitchDoc Labs <BR>
Grove Dust Sensor drivers for Raspberry Pi<BR>
Supports PPD42 Dust Sensor<BR>
https://shop.switchdoc.com/products/grove-dust-sensor
<BR>

Taken and modified from a variety of sources (see code)<BR>

Dust Sensor sourced from:

https://shop.switchdoc.com/products/grove-dust-sensor

Software: <BR>
Version 1.3<BR>

------------------<BR>
Installation<BR>
------------------<BR>

This software requires pigio in order to get accurate timings.

Install pigio as follows:

<pre>
sudo apt-get update
sudo apt-get install pigpio python-pigpio python3-pigpio
</pre>
<img src="http://www.switchdoc.com/wp-content/uploads/2018/09/IMG_7366.jpg" alt="Pi2Grover and Grove Dust Sesnor "  >

-----------------<BR>
Testing<BR>
-----------------<BR>

Hardware:  If you have Pi2Grover, plug your Grove Dust Unit into D4/D5.   That's it.
Otherwise, you need to write up the unit onto your GPIO on the Raspberry Pi.  We only support the Grove version at SwitchDoc Labs.
<BR>
Pi2Grover:  https://shop.switchdoc.com/products/pi2grover-raspberry-pi-to-grove-connector-interface-board
<BR>

To test, clone git repository into your Raspberry Pi Home Directory.  Then go into the directory
and edit testDust.py to change your GPIO pin number to match the Grove Plug you plugged it into.
<BR>
Start the pigpio daemon<BR>
<pre>
sudo pigpio
</pre>

Then run the testDust.py program:

<pre>
sudo python testDust.py
</pre>

You should (after 30 seconds) start to see output like this:

<pre>
Air Quality Measurements for PM2.5:
  1147 particles/0.01ft^3
  1 ugm^3
  Current AQI (not 24 hour avg): 7

Air Quality Measurements for PM2.5:
  1487 particles/0.01ft^3
  2 ugm^3
  Current AQI (not 24 hour avg): 9

Air Quality Measurements for PM2.5:
  6741 particles/0.01ft^3
  10 ugm^3
  Current AQI (not 24 hour avg): 43

Air Quality Measurements for PM2.5:
  2295 particles/0.01ft^3
  3 ugm^3
  Current AQI (not 24 hour avg): 14
</pre>



