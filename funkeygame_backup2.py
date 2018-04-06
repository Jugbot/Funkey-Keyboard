#!/usr/bin/env python
# rhythm game using ws2811 rgb leds
# format > python funkeygame.py <filename.mid>
import RPi.GPIO
import MCP230xx
import math
import time
import os

import Adafruit_GPIO as GPIO
import Adafruit_GPIO.I2C as I2C

mcp = MCP230xx.MCP23017()

import datetime
from random import random,seed
import colorsys
from threading import Thread

from pyllist import dllist, dllistnode

import midi
import sys

from neopixel import *

import scrollingtext
# Use busnum = 0 for older Raspberry Pi's (256MB)
#mcp = Adafruit_MCP230XX(busnum = 0, address = 0x20, num_gpios = 16)

# Set pins 0, 1 and 2 to output (you can set pins 0..15 this way)
for i in range(12):
    mcp.setup(i, GPIO.IN)
    mcp.pullup(i,True)

#print(pattern)
seed(time.time())
# LED strip configuration:
LED_COUNT = 100      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10       # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 128  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False

LEFT = 0
SELECT = 1
RIGHT = 2

START_DELAY = 3.0 #three seconds before song starts

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

def main():
    midifile = displaymenu(strip)        
    #read midi file and convert from relative time to absolute
    pattern = midi.read_midifile(midifile)
    pattern.make_ticks_abs()
    #convert beats per minute to seconds per LED
    bpm = 120.0
    spl = 60.0/bpm/2
    
    #convert midi events into an easier to read format
    notes = list(convertPattern(pattern, bpm))
    notes.sort()
    #local variables for rendering
    renderlist = dllist()
    i=0
    starttime = time.time()+START_DELAY
    while i < len(notes) or len(renderlist):
        print(i)
        while i < len(notes) and notes[i][0] < (time.time() - starttime) + spl * 8: #render one bar before press (one strip of LEDs)
            print(notes[i][0], time.time() - starttime)
            renderlist.append(Note(strip, notes[i], starttime, spl)) #TODO: might lag if notes are faster than it can render!
            i += 1
        for node in renderlist.iternodes():
            if not node.value.updateNote(): #rendersNote and returns whether or not note is still within scope
                renderlist.remove(node)
        #print([strip.getPixelColor(x) for x in range(strip.numPixels())])    
        strip.show()
        time.sleep(0.1)
    
    resetall(strip)
    strip.show()

    
class Note:
    def __init__(self, strip, data, starttime, spl):
        self.strip = strip
        self.start, self.stop, self.pitch = data
        self.offset = self.pitch % 12 * 8 #0-95
        self.flipped = (self.pitch % 2 == 0) #the hardware leds flip orientation every eight
        if self.offset > 100 - 8: #remove
            self.offset -= 96
        self.start += starttime                   #start of note press
        self.stop += starttime                    #end of note press
        self.spl = spl                     #seconds per led (one led = one eighth note or 1/2 beat)
        #print(self.spl)
        '''
        rcol = random()
        r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(rcol,0.5,1.0)] 
        self.color = Color(r, g, b)
        '''
        self.color = Color(0,255,0)
        #used by rendering
        self.laststart = 7
        self.laststop = 7
        #dubugging?
        self.name = midi.NOTE_NAMES[self.pitch % 12]
        #print(self.name)
    
    #controls the LEDs on a designated 8-LED strip
    #TODO: might need to stop calling time.time() so often
    def updateNote(self):        
        if self.stop < time.time(): #draw is done and should be removed
            return False
        if self.start > time.time() + self.spl * 8: #not ready to draw yet
            return True
        
        self.renderLED(self.start, self.laststart, self.color, True)
        self.renderLED(self.stop, self.laststop, Color(0,0,0), False)
            
        return True
    
    def renderLED(self, timestart, lastnote, color, leading):
        startLED = (timestart - time.time()) / self.spl
        absLED = int(math.ceil(startLED)) #absolute led index, where led is at full intensity
        remLED = absLED - startLED #remainder led, where led is at partial intensity
        if not leading:
            remLED = 1 - remLED #inverse remainder if it is not part of the leading end of lights
        if startLED < 0: #if the beginning of the note has passed but the ending has not
            if lastnote < 0:
                return
            absLED = 0
        
        for ledind in range(absLED, lastnote+1):
            if self.flipped:
                self.strip.setPixelColor(7-ledind + self.offset, color)                        
            else:
                self.strip.setPixelColor(ledind + self.offset, color)
        '''    
        if absLED > 0:
            cval = int(256*remLED)
            if self.flipped:
                self.strip.setPixelColor(7-(absLED-1) + self.offset, Color(cval,cval,cval))
            else:
                self.strip.setPixelColor(absLED-1 + self.offset, Color(cval,cval,cval))
        '''
        lastnote = absLED        
        
def secondsPerTick(bpm, res):
    return 60.0 / (bpm * res)

def convertPattern(pattern, bpm):
    spt = secondsPerTick(bpm, pattern.resolution)
    notestore = dllist()
    def addnotestore(notedata):
        if notedata[2] == False:
            for noteidx in range(len(notestore)):
                if notestore[noteidx][2] == True and notestore[noteidx][1] == notedata[1]:
                    note = notestore[noteidx]
                    del notestore[noteidx]
                    yield (note[0]*spt, notedata[0]*spt, note[1])
                    break
            else:
                print("Starting match not found for ", notedata)
        else:
            notestore.append(notedata)
                        
    for track in pattern:
        for event in track:
            if isinstance(event, midi.events.NoteOnEvent):
                if event.data[1] == 0:
                    for x in addnotestore((event.tick, event.data[0], False)):
                        yield x
                else:
                    for x in addnotestore((event.tick, event.data[0], True)):
                        yield x
            elif isinstance(event, midi.events.NoteOffEvent):
                for x in addnotestore((event.tick, event.data[0], False)):
                    yield x                
        
def lighttest(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(255,255,255))
    strip.show()
    time.sleep(1.0)
    
def resetall(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    
def displayLED(scrolling, strip):
    text = scrollingtext.LEDText(scrolling)
    
    while True:
        for ctr in range(text.loopcount()):
            curr_view = text.currentView()
            
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(0, 0, 0))

            for i in range(len(curr_view)):
                if not mcp.input(SELECT):
                    return SELECT
                if not mcp.input(LEFT):
                    return LEFT
                if not mcp.input(RIGHT):
                    return RIGHT
                if(curr_view[i]):
                    strip.setPixelColor(i, Color(200,0,0))
            strip.show()
            time.sleep(0.2)
            
            
        
def displaymenu(strip):
    path = os.path.join(os.getcwd(), "MidFiles")
    mid_files = os.listdir(path)

    index = 0
    
    displayLED("Please select a song", strip)
    resetall(strip)
    
    end = False
    while not end:
            
        dir = displayLED(mid_files[index].split(".mid")[0], strip)
        resetall(strip)

        if (dir == LEFT):
            index = (index - 1)%(len(mid_files))
        elif (dir == RIGHT):
            index = (index + 1)%(len(mid_files))
        elif (dir == SELECT):
            end = True
        
    return os.path.join(path, mid_files[index])

if __name__ == '__main__':
    while True:
        main()
    