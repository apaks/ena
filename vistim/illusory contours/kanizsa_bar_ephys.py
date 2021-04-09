# change the color of background (to black) for the positive control 
# psychopy code from https://www.programmingvisualillusionsforeveryone.online/scripts.html
# Alex Pak, 2017

import math, numpy, random #to have handy system and math functions 
from psychopy import core, event, visual, gui #these are the psychopy libraries
import serial, time

type = 1 #1 = Kanizsa ic, 2 = rotated pac man, 3 = square, 4 = line
ic_ori = 'h'
x,y = 0, 0 # set posiiton based on population RF responses 

myWin = visual.Window(color=-1, 
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
    radius = 125, 
    fillColor= 1, 
    lineColor=None)

def draw_4discs(a, x, y):
    disk.setPos([-a+x, y]) 
    disk.draw()
    disk.setPos([a+x, y])
    disk.draw()
    disk.setPos([x,a+y])
    disk.draw()
    disk.setPos([x,-a+y])
    disk.draw()

def draw_hor_sc(x,y):
    square_small.setPos([-250+x, y])
    square_small.draw()
    square_small.setPos([250+x, y])
    square_small.draw()
    # controls
    square_small_control.setPos([-x+50, 325+y])
    square_small_control.draw()
    square_small_control.setPos([x-50, -325+y])
    square_small_control.draw()
    
def draw_ver_sc(x,y):
    square_small.setPos([-x, 250+y])
    square_small.draw()
    square_small.setPos([x, -250+y])
    square_small.draw()
    #controls
    square_small_control.setPos([-x+350, 25+y])
    square_small_control.draw()
    square_small_control.setPos([x-350, -25+y])
    square_small_control.draw()
                
                
square = visual.Rect(myWin, width = 600, 
            height= 100, fillColor= -1, 
            lineColor=None)
            
if ic_ori != 'h':
    square.ori = 90
    
            
square_small = visual.Rect(myWin, width=150, 
            height=150, fillColor= -1, 
            lineColor=None)
            
square_small_control = visual.Rect(myWin, width=150, 
            height=150, fillColor= -1, ori = 60,
            lineColor=None)

if type == 4:
    square.lineColor = 1
    square.fillColor = -1
    square.lineWidth = 10
if type == 3:
    square.fillColor = 1
    
framerate=60 # Hz
duration = 0.5 # in sec
frames = int(duration*framerate)

if rec_flag==1:

    ser.write('3')
core.wait(4)
for i in range(trials):
    #t1 = time.time()
    print i
    if rec_flag==1:
        ser.write('1')
    core.wait(0.5)    
    #t2 = time.time()  
    for i in range(120):
        draw_4discs(300,x, y)
        myWin.flip()
    
    
    if type == 1:
        for i in range(frames):
            draw_4discs(300,x, y)
            if ic_ori == 'h':
                #makes illusion
                draw_hor_sc(x, y)
            else:
                # makes illusion
                draw_ver_sc(x, y)
                
            myWin.flip()
            
        myWin.flip()
    elif type == 2:
        for i in range(600):
            draw_4discs(300,x, y)
            square_small_control.setPos([-x+50, 325+y])
            square_small_control.draw()
            square_small_control.setPos([x-50, -325+y])
            square_small_control.draw()
            square_small_control.setPos([-x+350, 25+y])
            square_small_control.draw()
            square_small_control.setPos([x-350, -25+y])
            square_small_control.draw()
            myWin.flip()
        myWin.flip()
    else:
        for i in range(600):
            draw_4discs(300,x, y)
            if ic_ori == 'h':
                draw_hor_sc(x, y)
                square.setPos([x, y])
                square.draw()
                
            else:
                # makes illusion
                draw_ver_sc(x, y)                
                square.setPos([x, y])
                square.draw()
                
            myWin.flip()
        myWin.flip()
    #print t2 - t1
    core.wait(12)  #waits for 5 seconds

myWin.close() #closes the window
core.quit() #quits


