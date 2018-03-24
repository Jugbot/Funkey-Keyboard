#!/usr/bin/env python2.7
# Based on NeoPixel library and strandtest example by Tony DiCola (tony@tonydicola.com)
# To be used with a 12x1 NeoPixel LED stripe.
# Place the LEDs in a circle an watch the time go by ...
# red = hours
# blue = minutes 1-5
# green = seconds
# (To run the program permanently and with autostart use systemd.)

import time
import datetime
import math
from random import random
import colorsys
from threading import Thread

from pyllist import dllist, dllistnode

import midi
import sys
import curses

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()


#from neopixel import *
'''
if len(sys.argv) != 2:
    print "Usage: {0} <midifile>".format(sys.argv[0])
    sys.exit(2)
'''
midifile = "dq.mid"
#print(pattern)

# LED strip configuration:
LED_COUNT = 50      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10       # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False

START_DELAY = 3.0 #delay in seconds before the song starts


def main():
    pattern = midi.read_midifile(midifile)
    pattern.make_ticks_abs()
    bpm = 120.0
    spl = 60.0/bpm/2
    
    # Create NeoPixel object with appropriate configuration.
    #strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    #strip.begin()
    #strip.setBrightness(20)
    strip = [' '] * 50
    '''
    lighttest(strip)
    resetall(strip)
    strip.show()
    '''
    notes = list(convertPattern(pattern, bpm))
    notes.sort()
    '''
    for i in range(len(notes)):
        stdscr.addstr(i,0,str(notes[i]))
    stdscr.refresh()
    time.sleep(4.0)
    '''
    #notes.append((None, None, None))

    renderlist = dllist()

    i=0
    starttime = time.time()+START_DELAY
    while (i < len(notes) or len(renderlist)) :
        #print(i)
        stdscr.addstr(11,0,"        ")
        stdscr.addstr(10,0,"        ")
        stdscr.addstr(9,0,"        ")
        stdscr.addstr(7,0,"        ")
        stdscr.addstr(8,0,"        ")
        while i < len(notes) and notes[i][0] < (time.time() - starttime) + spl * 8: #render one bar before press (one strip of LEDs)
            #print(notes[i][0], time.time() - starttime)
            stdscr.addstr(10,0,"add")
            renderlist.append(Note(strip, notes[i], starttime, spl)) #TODO: might lag if notes are faster than it can render!
            i += 1
        stdscr.addstr(15, 0, str(time.time() - starttime))
        for node in renderlist.iternodes():
            if not node.value.updateNote(): #rendersNote and returns whether or not note is still within scope
                renderlist.remove(node)
                stdscr.addstr(9,0,"remove")
        #print([strip.getPixelColor(x) for x in range(strip.numPixels())])    
        for x in range(0, 50/8):
            stdscr.addstr(x, 0, str(strip[x*8:(x+1)*8]))
        stdscr.addstr(7,0,str(i) + " / " + str(len(notes)))
        stdscr.addstr(8,0,str(len(renderlist)))
        stdscr.refresh()
        # for z in range(len(strip)):
        #     strip[z] = ' '
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    '''
    resetall(strip)
    strip.show()'''

    
class Note:
    def __init__(self, strip, data, starttime, spl):
        self.strip = strip
        self.start, self.stop, self.pitch = data
        self.offset = self.pitch % 12 * 8 #0-95
        self.flipped = (self.pitch % 2 == 0) #the hardware leds flip orientation every eight
        self.flipped = False
        #self.flipped = False #remove
        if self.offset > 50 - 8: #remove
            self.offset -= 48
            #self.offset = 0 #remove
        self.start += starttime                   #start of note press
        self.stop += starttime                    #end of note press
        self.spl = spl                     #seconds per led (one led = one eighth note or 1/2 beat)
        #print(self.spl)
        rcol = random()
        r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(rcol,1.0,0.5)] #TODO: fix
        self.color = None#Color(255, 255, 255) #change
        #used by rendering
        self.laststart = 7
        self.laststop = 7
        self.name = midi.NOTE_NAMES[self.pitch%12]
        stdscr.addstr(11, 0, self.name)
    
    #controls the LEDs on a designated 8-LED strip
    #TODO: might need to stop calling time.time() so often
    def updateNote(self):
        #print("draw start", self.start, self.stop, time.time())
        
        if self.stop < time.time(): #draw is done and should be removed
            return False
        if self.start > time.time() + self.spl * 8: #not ready to draw yet
            return True
        
        self.renderstartLED()
        self.renderstopLED()        
            
        return True
    
    def renderstartLED(self):
        startLED = int((self.start - time.time()) / self.spl)
        if startLED < 0: #if the beginning of the note has passed but the ending has not
            return
        
        if self.flipped:
            for ledind in range(self.laststart, startLED+1):
                self.strip[7-ledind + self.offset] = '1'#self.strip.setPixelColor(7-ledind + self.offset, self.color)
        else:
            for ledind in range(self.laststart, startLED+1):
                self.strip[ledind + self.offset] = '1'#pass#self.strip.setPixelColor(ledind + self.offset, self.color)
        self.laststart = startLED
            
    def renderstopLED(self):
        stopLED = int((self.stop - time.time()) / self.spl)
        if stopLED > 7: #end of note press has not appeared
            return
        
        if self.flipped:
            for ledind in range(self.laststop, stopLED+1):
                self.strip[7-ledind + self.offset] = ' '
                #self.strip.setPixelColor(7-ledind + self.offset, Color(0,0,0))
        else:
            for ledind in range(self.laststop, stopLED+1):
                self.strip[ledind + self.offset] = ' '
                #self.strip.setPixelColor(ledind + self.offset, Color(0, 0, 0))
        self.laststop = stopLED
        
        
def secondsPerTick(bpm, res):
    return 60.0 / (bpm * res)

def convertPattern(pattern, bpm):
    spt = secondsPerTick(bpm, pattern.resolution)
    notestore = dllist()
    def addnotestore(notedata):
        #print notestore
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
            #elif isinstance(event, midi.events.EndOfTrackEvent):
            #    yield (None, None, None)
                
'''
def lighttest(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(255,255,255))
    strip.show()
    time.sleep(1.0)
    
def resetall(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))        

def update(strip, data, bpm=120.0):
    start, stop, pitch = data
    bpm = 60.0/bpm
    notepos = 1.0
    lastpos = 0
    while (notepos < 100):
        timestart = time.time()
        fallingLED = int(notepos % strip.numPixels())
        risingStrength = int((notepos % strip.numPixels() - fallingLED) * 256)
        risingLED = (fallingLED + 1) % strip.numPixels()
        fallingStrength = 255 - risingStrength
        #print(strip.numPixels(), int(notepos), strip.numPixels() % int(notepos))
        
        strip.setPixelColor(lastpos, Color(0,0,0))
        strip.setPixelColor(risingLED, Color(risingStrength,risingStrength,risingStrength))
        strip.setPixelColor(fallingLED, Color(fallingStrength,fallingStrength,fallingStrength))
        lastpos = fallingLED
        strip.show()
        
        #must move 2 leds every beat
        notepos += (time.time()-timestart) / (bpm) * 4 #time elapsed / time per beat * leds per beat
'''
if __name__ == '__main__':
    main()
    