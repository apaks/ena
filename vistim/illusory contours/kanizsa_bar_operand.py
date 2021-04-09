# change the color of background (to black) for the positive control 
# psychopy https://www.programmingvisualillusionsforeveryone.online/scripts.html

import math, numpy, random #to have handy system and math functions 
from psychopy import core, event, visual, gui #these are the psychopy libraries
import serial


ic = True
rot = False
myWin = visual.Window(color=0, 
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
    radius=60, 
    fillColor= -1, 
    lineColor=None)

square = visual.Rect(myWin, width = 70, 
            height=250, fillColor=-1, 
            lineColor=None)
            
square2 = visual.Rect(myWin, width = 50, 
            height=230, fillColor= -1, 
            lineColor=None)
square_small = visual.Rect(myWin, width=70, 
            height=100, fillColor= 0, 
            lineColor=None)

if rec_flag==1:

    ser.write('3')

for i in range(trials):
    
    #disk.setPos([0,-125]) 
    #disk.draw()
    #disk.setPos([0,125])
    #disk.draw()
    disk.setPos([-125,0])
    disk.draw()
    disk.setPos([125,0])
    disk.draw()
    myWin.flip()
    core.wait(0.5)
    
    
    if rec_flag==1:
        ser.write('1')
        
    if ic == True:
        
        #disk.setPos([0,-125]) 
        #disk.draw()
        #disk.setPos([0,125])
        #disk.draw()
        disk.setPos([-125,0])
        disk.draw()
        disk.setPos([125,0])
        disk.draw()
        
        square_small.setPos([-155, -50])
        square_small.setOri(30)
        square_small.draw()
        square_small.setPos([150, 50])
        square_small.draw()
        
    
    if rot == True:
        square_small.setPos([-25, -175])
        square_small.setOri(30)
        square_small.draw()
        square_small.setPos([25, 175])
        square_small.draw()

    else:
        square.draw()
        #square2.draw()
       
    myWin.flip()
    

    core.wait(10)  #waits for 5 seconds
    myWin.flip()
    core.wait(5)

myWin.close() #closes the window
core.quit() #quits


