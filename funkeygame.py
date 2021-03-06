#!/usr/bin/env python
# rhythm game using ws2811 rgb leds
import math
import os
import time
import colorsys
from random import seed, random
from multiprocessing import Process, Queue

import Adafruit_GPIO as GPIO
import MCP230xx
import midi
from scrollingtext import LEDText
from neopixel import *
from pyllist import dllist
import vlc

# Set the port expander global variable
#mcp = MCP230xx.MCP23017()

# Set pins 0-11 to output and pullup(you can set pins 0..15 this way)
for i in xrange(12):
    pass
    #mcp.setup(i, GPIO.IN)
    #mcp.pullup(i, True)

# Seed random
seed(time.time())

# LED strip configuration:
LED_COUNT = 96  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 64  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
# Menu select buttons indexes
LEFT = 0
SELECT = 1
RIGHT = 2
# three seconds before song starts
START_DELAY = 3.0


def main(strip):

    # Get midi file from menu select
    # midifile = songselectmenu(strip)
    
    path = os.path.join(os.getcwd(), "MidFiles")
    file = os.path.splitext(os.listdir(path)[0])[0]
    midifile = os.path.join(path, file + ".mid")
    mp3file = os.path.join(path, file + ".mp3")

    # read midi file and convert from relative time to absolute
    pattern = midi.read_midifile(midifile)
    pattern.make_ticks_abs()

    # convert beats per minute to seconds per LED
    bpm = 120.0
    spl = 60.0 / bpm / 2

    # convert midi events into an easier to read format
    notes = list(convertPattern(pattern, bpm))
    notes.sort()

    result = Queue()
    starttime = time.time() + START_DELAY
    # input loop
    #input_thread = Process(target=inputloop, args=(notes, starttime, result))
    #input_thread.start()
    # render loop
    
    playsongmp3(mp3file)
    renderloop(notes, spl, strip, starttime)
    
    #input_thread.join()

    #end
    resetall(strip)
    strip.show()
    
def playsongmp3(url):
    p = vlc.MediaPlayer(url)
    p.play()

def inputloop(args):
    notes, starttime, result = args
    perfect_tolerance = 0.1 #radial tolerance of hitting the note perfectly
    hit_tolerance = 0.5 #tolerance where hitting the key counts as hitting the note
    last_note = notes[-1][0]
    presses = []
    score = 0
    b_state = [0] * 12
    gpio_i = range(12)
    while time.time()-starttime < last_note + hit_tolerance:
        for b_i in gpio_i:
            state = True#mcp.input(b_i)
            if state != b_state[b_i]:
                # ( time, button index, state <begin or end> )
                presses.append((time.time()-starttime, b_i, state))
                b_state[b_i] = state
    # song ends calc score out of 10000
    note_ind = 0
    last_possible = None
    for press in presses:
        while press[0] < notes[note_ind][0] + hit_tolerance:
            if press[0] < notes[note_ind][0] - hit_tolerance:
                last_possible = note_ind
            if press[2] == notes[note_ind][2] \
                    and press[1] == notes[note_ind][1]\
                    and -hit_tolerance < press[0] - notes[note_ind][0] < hit_tolerance:
                if -perfect_tolerance < press[0] - notes[note_ind][0] < perfect_tolerance:
                    score += 1
                note_ind = last_possible
                break
            note_ind += 1



    result.put(score/len(notes)*10000)

def renderloop(notes, spl, strip, starttime):
    # local variables for rendering
    renderlist = dllist()
    i = 0
    while i < len(notes) or len(renderlist):
        # print(i)
        while i < len(notes) and notes[i][0] < (time.time() - starttime) + spl * 8:  # render one bar before press (one strip of LEDs)
            # print(notes[i][0], time.time() - starttime)
            if notes[i][2] in range(midi.NOTE_NAME_MAP_SHARP['C_5'], midi.NOTE_NAME_MAP_SHARP['C_6']):
                renderlist.append(
                    Note(strip, notes[i], starttime, spl))  # TODO: might lag if notes are faster than it can render!
            i += 1
        for node in renderlist.iternodes():
            if not node.value.updateNote():  # rendersNote and returns whether or not note is still within scope
                renderlist.remove(node)
        # print([strip.getPixelColor(x) for x in xrange(strip.numPixels())])
        strip.show()



class Note:
    def __init__(self, strip, data, starttime, spl):
        self.strip = strip
        self.start, self.stop, self.pitch = data
        self.offset = self.pitch % 12 * 8  # 0-95
        self.flipped = (self.pitch % 2 == 0)  # the hardware leds flip orientation every eight
        if self.offset > strip.numPixels() - 8:  # remove
            self.offset -= strip.numPixels() - strip.numPixels() % 8
        self.start += starttime  # start of note press
        self.stop += starttime  # end of note press
        self.spl = spl  # seconds per led (one led = one eighth note or 1/2 beat)
        # Random color per note idea (unfinished)
        rcol = random()
        r,g,b = [int(256*i) for i in colorsys.hls_to_rgb(rcol,0.5,1.0)] 
        self.color = Color(r, g, b)
        self.color = Color(255, 255, 255)
        # used by rendering
        self.laststart = 7
        self.laststop = 7
        # dubugging?
        self.name = midi.NOTE_NAMES[self.pitch % 12]
        # print(self.name)

    # controls the LEDs on a designated 8-LED strip
    def updateNote(self):
        if self.stop < time.time():  # draw is done and should be removed
            return False
        if self.start > time.time() + self.spl * 8:  # not ready to draw yet
            return True

        self.renderLED(self.start, self.laststart, self.color, True)
        self.renderLED(self.stop, self.laststop, 0, False)

        return True

    # render LEDs
    def renderLED(self, timestart, lastnote, color, leading):
        startLED = (timestart - time.time()) / self.spl
        absLED = int(math.ceil(startLED))  # absolute led index, where led is at full intensity
        remLED = absLED - startLED  # remainder led, where led is at partial intensity
        if not leading:
            remLED = 1 - remLED  # inverse remainder if it is not part of the leading end of lights
        if startLED < 0:  # if the beginning of the note has passed but the ending has not
            if lastnote < 0:
                return
            absLED = 0

        for ledind in xrange(absLED, lastnote + 1):
            if not self.flipped:
                self.strip.setPixelColor(7 - ledind + self.offset, color)
            else:
                self.strip.setPixelColor(ledind + self.offset, color)

        if absLED > 0:
            cval = int(256 * remLED)
            if not self.flipped:
                self.strip.setPixelColor(7 - (absLED - 1) + self.offset, Color(cval, cval, cval))
            else:
                self.strip.setPixelColor(absLED - 1 + self.offset, Color(cval, cval, cval))

        lastnote = absLED


# BPM to SPT
def secondsPerTick(bpm, res):
    return 60.0 / (bpm * res)


# Converting midi pattern into a more readable format
def convertPattern(pattern, bpm):
    spt = secondsPerTick(bpm, pattern.resolution)
    notestore = dllist()

    def addnotestore(notedata):
        if notedata[2] == False:
            for noteidx in xrange(len(notestore)):
                if notestore[noteidx][2] == True and notestore[noteidx][1] == notedata[1]:
                    note = notestore[noteidx]
                    del notestore[noteidx]
                    yield (note[0] * spt, notedata[0] * spt, note[1])
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
                    # Wipe strip


def resetall(strip):
    for i in xrange(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def wheel(pos):
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

# Menu, shows scrolling text .split(".")[0]
def songselectmenu(strip):
    path = os.path.join(os.getcwd(), "MidFiles")
    mid_files = os.listdir(path)

    index = 0
    resetall(strip)

    ledtext = LEDText("Select A Song!  ", 12, 8)
    canend = False
    while True:
        ledtext.nextview()
        for strip_i, led in zip(xrange(strip.numPixels()), ledtext):
            if led:
                strip.setPixelColor(strip_i, wheel((strip_i - int(time.time()*100)) & 255))
            else:
                strip.setPixelColor(strip_i, 0)
        strip.show()
        time.sleep(0.05)

        left = True#mcp.input(LEFT)
        select = True#mcp.input(SELECT)
        right = True#mcp.input(RIGHT)

        if (left):
            index = (index - 1) % (len(mid_files))
            canend = True
        elif (right):
            index = (index + 1) % (len(mid_files))
            canend = True
        elif select and canend:
            return os.path.join(path, mid_files[index])



# DEBUG
def lighttest(strip):
    for i in xrange(strip.numPixels()):
        strip.setPixelColor(i, Color(255, 255, 255))
    strip.show()
    time.sleep(1.0)


if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    try:
        while True:
            main(strip)
    except KeyboardInterrupt:
        print("W: interrupt received, stopping...")
    finally:
        # clean up
        resetall(strip)
