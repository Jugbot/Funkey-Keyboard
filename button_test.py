import RPi.GPIO
import MCP230xx
import math
import time

import Adafruit_GPIO as GPIO
import Adafruit_GPIO.I2C as I2C
# Use busnum = 0 for older Raspberry Pi's (256MB)
#mcp = Adafruit_MCP230XX(busnum = 0, address = 0x20, num_gpios = 16)
# Use busnum = 1 for new Raspberry Pi's (512MB with mountingholes)
while True:
    try:
        mcp = MCP230xx.MCP23017()
        # Set pins 0, 1 and 2 to output (you can set pins 0..15 this way)
        for i in range(12):
            mcp.setup(i, GPIO.IN)
            mcp.pullup(i,True)
         
        # Set pin 3 to input with the pullup resistor enabled
        #mcp.pullup(3, 1)
        # Read pin 3 and display the results
        while (True):
            for i in range(12):
                print "%d: %x" % (i, mcp.input(i))
            time.sleep(0.1)
        exit(1)
        
    except IOError as e:
        print(e)
    mcp = MCP230xx.MCP23017()
    time.sleep(1)
 
