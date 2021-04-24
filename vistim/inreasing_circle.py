from __future__ import division
from psychopy import core, event, visual, gui #these are the psychopy libraries
import numpy as np

r = 10
myWin = visual.Window(color='grey', 
        units='pix', size=[1920,1080], 
        screen = 2,
        allowGUI=False, 
        fullscr=False) #creates a window

disc = visual.Circle(myWin, 
    radius=r, 
    fillColor='black', 
    vertices = 128,
    lineColor = None)
    
ls_stim = []
for r in range(200):
    disc = visual.Circle(myWin, 
    radius=r, 
    fillColor='black', 
    vertices = 128,
    lineColor = None)
    ls_stim.append(disc)


    
core.wait(5)
for tr in range(10):
#    for i in range(10):
#        disc.size = 10*i
#        disc.draw()
#        core.wait(0.1)
#        myWin.flip()
#    myWin.flip()    
    for stim in ls_stim:
        stim.draw()
        myWin.flip()
    myWin.flip()    
core.wait(10)

