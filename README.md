# Funkey-Keyboard ヽ(⌐■_■)ノ♪♬
### A piano with a built-in rhythm game! 
This was a project for New York University's prototyping design class (EG1003) for spring of 2018. The design won the Nick Russo Award and the I2E Award for Innovation.  

The idea behind this prototype was to make learning the piano easier by turning it into a sort of rhythm game. Other similar solutions exist out there such as [pianos that light up the next keys](https://www.smartpiano.com/) or tablet apps that record audio from an existing piano and use it as an input for a a [game-like learning tool](https://www.synthesiagame.com/).

Check out the [video demonstration](https://youtu.be/wlrPzlZg1Dw).

| Implemented | <ul><li>Automatic conversion of midi files to playable songs</li><li>Real time playback</li><li>Pseudo-random color change for differentiating notes</li></ul> |
| :--- | :--- |
| Unimplemented | <ul><li>Tempo must be input manually (bpm variable in code)</li><li>The circuit board for the buttons failed, so input recording and scoring was not able to be tested</li><li>As such the menu with scrolling text is not used in the last release and songs must be set beforehand in-code</li></ul> |

## Dependencies:
+ pyllist
+ python-midi
+ adafruit-gpio

___
## Hardware
I used the [ws2811 addressable rgb led string](http://a.co/irZiaNd) as a display.

For the inputs I decided to use [mcp23017 io port expander](https://www.adafruit.com/product/732) to demonstrate the possibility of modularity. 

![Image of ortho explode view](/images/explode.png)

Button Input/ LED Mount | Electrical Schematic 
----------------------- | -------------------- 
<img src="/images/pcb.jpg" alt="Image of pcb board" /> | <img src="/images/schematic.jpg" alt="Image of electrical schematic" />
