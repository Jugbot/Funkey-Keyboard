import time

LIBRARY = { "A": [1,1,1,1,1,1,1,1,
                    0,0,0,1,0,0,0,1,
                    1,0,0,0,1,0,0,0,
                    0,0,0,1,0,0,0,1,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "B": [1,1,1,0,0,1,1,1,
                    1,1,0,1,1,0,1,1,
                    1,1,0,1,1,0,1,1,
                    1,1,0,1,1,0,1,1,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "C": [1,0,0,0,0,0,0,1,
                    1,0,0,0,0,0,0,1,
                    1,0,0,0,0,0,0,1,
                    1,0,0,0,0,0,0,1,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "D": [0,0,0,1,1,0,0,0,
                    0,0,1,0,0,1,0,0,
                    0,0,1,0,0,1,0,0,
                    0,1,0,0,0,0,1,0,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "E": [1,0,0,1,1,0,0,1,
                    1,0,0,1,1,0,0,1,
                    1,0,0,1,1,0,0,1,
                    1,0,0,1,1,0,0,1,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "F": [1,0,0,1,1,0,0,0,
                    0,0,0,1,1,0,0,1,
                    1,0,0,1,1,0,0,0,
                    0,0,0,1,1,0,0,1,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "G": [1,0,0,0,1,1,1,1,
                    1,0,0,1,0,0,0,1,
                    1,0,0,0,1,0,0,1,
                    1,0,0,0,0,0,0,1,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "H": [1,1,1,1,1,1,1,1,
                    0,0,0,1,1,0,0,0,
                    0,0,0,1,1,0,0,0,
                    0,0,0,1,1,0,0,0,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "I": [1,0,0,0,0,0,0,1,
                    1,0,0,0,0,0,0,1,
                    1,1,1,1,1,1,1,1,
                    1,0,0,0,0,0,0,1,
                    1,0,0,0,0,0,0,1,
                    0,0,0,0,0,0,0,0],
              "J": [0,0,0,0,1,1,1,1,
                    1,0,0,0,0,0,0,1,
                    1,0,0,0,0,0,0,1,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,1,
                    0,0,0,0,0,0,0,0],
              "K": [1,0,0,0,0,0,0,1,
                    0,1,0,0,0,0,1,0,
                    0,0,1,0,0,1,0,0,
                    0,0,0,1,1,0,0,0,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "L": [0,0,0,0,0,0,0,1,
                    1,0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,1,
                    1,0,0,0,0,0,0,0,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "M": [1,1,1,1,1,1,1,1,
                    0,0,0,1,1,0,0,0,
                    0,0,0,0,0,1,1,0,
                    0,0,0,1,1,0,0,0,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "N": [1,1,1,1,1,1,1,1,
                    0,0,1,1,0,0,0,0,
                    0,0,0,1,1,0,0,0,
                    0,0,1,1,0,0,0,0,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "O": [0,0,1,1,1,1,0,0,
                    1,1,0,0,0,0,1,1,
                    1,1,0,0,0,0,1,1,
                    1,1,0,0,0,0,1,1,
                    0,0,1,1,1,1,0,0,
                    0,0,0,0,0,0,0,0],
              "P": [0,1,1,1,0,0,0,0,
                    0,0,0,0,1,0,0,1,
                    1,0,0,1,0,0,0,0,
                    0,0,0,0,1,0,0,1,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "Q": [1,1,1,1,1,1,1,1,
                    1,1,0,0,0,0,0,1,
                    1,0,0,0,1,1,0,1,
                    1,0,0,0,0,0,0,1,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "R": [0,1,1,0,1,1,1,1,
                    0,0,0,0,1,0,0,1,
                    1,0,0,1,0,0,0,0,
                    0,0,0,0,1,0,0,1,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "S": [1,0,0,0,1,1,1,1,
                    1,0,0,1,0,0,0,1,
                    1,0,0,0,1,0,0,1,
                    1,0,0,1,0,0,0,1,
                    1,1,1,1,0,0,0,1,
                    0,0,0,0,0,0,0,0],
              "T": [1,1,0,0,0,0,0,0,
                    0,0,0,0,0,0,1,1,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,1,1,
                    1,1,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,0],
              "U": [1,1,1,1,1,1,1,1,
                    1,1,0,0,0,0,0,0,
                    0,0,0,0,0,0,1,1,
                    1,1,0,0,0,0,0,0,
                    1,1,1,1,1,1,0,0,
                    0,0,0,0,0,0,0,0],
              "V": [1,1,1,1,0,0,0,0,
                    0,0,1,0,0,0,0,0,
                    0,0,0,0,0,0,1,0,
                    0,0,1,0,0,0,0,0,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "W": [1,1,1,1,1,1,1,1,
                    0,0,0,1,1,0,0,0,
                    0,1,1,0,0,0,0,0,
                    0,0,0,1,1,0,0,0,
                    1,1,1,1,1,1,1,1,
                    0,0,0,0,0,0,0,0],
              "X": [1,1,0,0,0,0,1,1,
                    0,0,1,1,1,1,0,0,
                    0,0,1,1,1,1,0,0,
                    1,1,0,0,0,0,1,1],
              "Y": [1,0,0,0,0,0,0,0,
                    0,0,0,0,0,0,1,0,
                    0,0,1,1,1,1,1,1,
                    0,0,0,0,0,0,1,0,
                    1,0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,0],     
              "Z": [1,1,0,0,0,0,0,1,
                    1,0,0,0,1,1,0,1,
                    1,0,0,0,1,1,0,1,
                    1,1,0,0,0,0,0,1],
              " ": [0,0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,0]}

class LEDText:
    def __init__(self, theS):
        self.row = 8
        self.col = 12
        theS = theS.split(".")[0].upper()
        self.s = ""
        for i in theS:
            if i in "ABCEFGHIJKLMNOPQRSTUVWXYZ":
                self.s += i
            else:
                self.s += " "
        self.lst = []
        for i in self.s:
            self.lst.extend(LIBRARY[i][::-1])
        # print self.lst
        self.index = 0
    
    def loopcount(self):
        return (len(self.lst)-self.row/self.col)/self.row/2+1
    
    def currentView(self):
        templst = self.lst[(self.index) : ((self.row*self.col)+self.index)][::-1]
        self.index = (self.index + self.row*2) % len(self.lst)
        return templst
