from lbdict import LetterBitmapDictionary
import os

def makeLibrary():
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "Font/kongtext.ttf"
    rel_path_save = "Font/"
    abs_font_path = os.path.join(script_dir, rel_path)
    abs_save_dir = os.path.join(script_dir, rel_path_save)
    return LetterBitmapDictionary(abs_font_path, 8, abs_save_dir, transposed=True, sety=8)

LIBRARY = makeLibrary()

class LEDText:
    def __init__(self, text, width, height):
        self.height = height
        self.width = width
        self.text = text
        self.textgen = TextGenerator(self.text)
        self.scrollindex = 0
        self.display = [False] * (width * height)
        #self._last_pos = None
        self._init_led_states()

    def _init_led_states(self):
        for x in xrange(self.width):
            col = next(self.textgen)
            for y in xrange(len(col)):
                self.display[x*self.height + y] = col[y]

    def __iter__(self): #reversing
        for x in xrange(self.width):
            for y in xrange(self.height):
                if x % 2 == 0:
                    yield self.display[x*self.height + y]
                else:
                    yield self.display[x*self.height + (self.height - 1 - y)] #invert column

    def nextview(self):
        start = self.scrollindex * self.height
        l2 = next(self.textgen)
        for l_i in xrange(len(l2)):
            self.display[start + l_i] = l2[l_i]
        self.scrollindex = (self.scrollindex + 1) % self.width

class TextGenerator(object):
    def __init__(self, text):
        self.text = text
        self.char_lst = None
        self.text_ind = 0
        self.col_ind = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.next()

    def next(self):
        if self.char_lst is None:
            self.char_lst = LIBRARY[self.text[self.text_ind]]
        col = self.char_lst[self.col_ind]
        self.col_ind += 1
        if self.col_ind == len(self.char_lst):
            self.col_ind = 0
            self.text_ind += 1
            if self.text_ind == len(self.text):
                self.text_ind = 0
            self.char_lst = LIBRARY[self.text[self.text_ind]]
        return col
