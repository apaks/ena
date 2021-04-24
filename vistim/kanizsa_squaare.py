# change the color of background (to black) for the positive control 
# psychopy code from https://www.programmingvisualillusionsforeveryone.online/scripts.html
# Alex Pak, 2017

import math, numpy, random #to have handy system and math functions 
from psychopy import core, event, visual, gui #these are the psychopy libraries
import serial

ic = 1 # 1=True, 0 False, illusinory contours
rot = 1 # rotated pac-man inducers controls
seq = 1 # incuders first then subjective contour
line = 0

x,y = 150, 100 # set posiiton based on population RF responses 

myWin = visual.Window(color='grey', 
        units='pix', size=[1920,1080], 
        allowGUI=True, 
        fullscr=False) #creates a window

#myClock = core.Clock() #this creates and starts a clock which we can later read
rec_flag = 0
trials = 20


if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)
    trials = 20

disk = visual.Circle(myWin, 
    radius=125, 
    fillColor='black', 
    lineColor=None)

def draw_4discs(a, x, y):
    disk.setPos([-a+x,-a+y]) 
    disk.draw()
    disk.setPos([a+x,-a+y])
    disk.draw()
    disk.setPos([-a+x,a+y])
    disk.draw()
    disk.setPos([a+x,a+y])
    disk.draw()

square = visual.Rect(myWin, width = 600, 
            height=600, fillColor='grey', 
            lineColor=None)
            

            
square_small = visual.Rect(myWin, width=150, 
            height=150, fillColor='grey', 
            lineColor=None)
if ic==0:
    square.fillColor = 'white'
if line == 1:
    square.lineColor = 'black'
    square.fillColor = 'grey'
    
if rec_flag==1:

    ser.write('3')
core.wait(4)
for i in range(trials):
    print i
    if rec_flag==1:
        ser.write('1')
    core.wait(0.5)    
    if seq == 1: 
        draw_4discs(300,x, y)
        myWin.flip()
      
        
    if ic == True:
        draw_4discs(300,x, y)

    if rot == True:
        core.wait(0.5)  
        square_small.setPos([-375+x, -375+y])
        square_small.draw()
        square_small.setPos([375+x, 375+y])
        square_small.draw()
        square_small.setPos([-375+x, 375+y])
        square_small.draw()
        square_small.setPos([375+x, -375+y])
        square_small.draw()

    else:
        core.wait(0.5)
        square.setPos([x, y])
        square.draw()
       
    myWin.flip()

    core.wait(0.5)  #waits for 5 seconds
    myWin.flip()
    core.wait(7)
myWin.close() #closes the window
core.quit() #quits


