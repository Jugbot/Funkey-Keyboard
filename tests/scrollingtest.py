import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scrollingtext'))
from scrollingtext import LEDText

test = LEDText("hello thar...", 12, 8)
while True:
    lst = list(test)
    for y in range(8):
        for x in range(12):
            print('#' if lst[x*8 +y] else '-'),
        print()

    test.nextview()