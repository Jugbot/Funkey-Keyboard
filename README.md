# Funkey-Keyboard ヽ(⌐■_■)ノ♪♬
### A piano with a built-in rhythm game! 
This was a project for New York University's prototyping design class (EG1003) for spring of 2018. The design won the Nick Russo Award and the I2E Award for Innovation.  

Check out the [video demonstration](https://youtu.be/wlrPzlZg1Dw).

| Implemented | - Automatic conversion of midi files to playable songs<br>- Real time playback<br>- Pseudo-random color change for differentiating notes |
| :--- | :--- |
| Unimplemented | - Tempo must be input manually (bpm variable in code)<br>- The circuit board for the buttons failed, so input recording and scoring was not able to be tested<br>- As such the menu with scrolling text is not used in the last release and songs must be set beforehand in-code |

## Dependencies:
+ pyllist
+ python-midi
+ adafruit-gpio

___
## Hardware
I used the [ws2811 addressable rgb led string](http://a.co/irZiaNd) as a display.

For the inputs I decided to use [mcp23017 io port expander](https://www.adafruit.com/product/732) to demonstrate the possibility of modularity. 

![Image of ortho explode view](/images/explode.png)
| ![Image of electrical schematic](/images/schematic.jpg) | ![Image of pcb board](/images/pcb.jpg) |
| --- | --- |


