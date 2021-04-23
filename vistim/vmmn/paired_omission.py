
# Alex Pak, 2017
# Trial duration 1.5 s

from __future__ import division
from psychopy import visual, core #import some libraries from PsychoPy
import time
import serial
from random import randint
from scipy import random 
import numpy as np

trial_type = ['ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 
'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 
'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 
'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 
'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 
'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 
'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 
'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 
       'ab', 'ab', 'ab', 'ab', '--', 'ab', 'ab', 'ab', 'ab', 'ab', 'a-',
       'ab', 'ab', 'a-', 'b-', 'ab', 'ab', 'ab', 'ab', 'a-', 'ab', 'ab',
       'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'b-', 'ab', 'b-',
       'ab', 'ab', 'ab', 'a-', 'a-', 'ab', 'b-', 'ab', '--', 'ab', 'ab',
       'b-', '--', 'ab', 'ab', 'b-', 'ab', 'a-', 'b-', 'ab', 'ab', 'ab',
       'ab', 'ab', 'b-', 'ab', 'ab', 'ab', 'ab', '--', 'ab', 'ab', 'a-',
       'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'b-', 'ab', 'b-', '--', 'ab',
       'a-', 'ab', '--', 'ab', 'ab', 'ab', '--', 'ab', 'ab', 'ab', 'ab',
       'a-', 'ab', 'ab', 'ab', '--', 'a-', 'b-', 'ab', 'ab', 'ab', 'ab',
       'a-', 'ab', 'ab', 'ab', 'ab', 'ab', 'b-', 'ab', 'ab', 'ab', 'ab',
       'ab', 'a-', 'b-', 'ab', 'ab', 'b-', 'ab', 'ab', 'ab', 'ab', 'ab',
       'ab', 'b-', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab',
       'b-', 'ab', '--', 'ab', 'ab', 'ab', 'a-', 'ab', '--', 'ab', 'ab',
       'ab', 'ab', 'ab', 'a-', 'a-', 'ab', 'ab', 'ab', '--', 'ab', 'ab',
       '--', 'ab', 'ab', '--', 'ab', 'ab', 'b-', 'ab', 'ab', '--', 'a-',
       'ab', '--', 'ab', 'b-', 'a-', 'ab', '--', 'ab', 'ab', 'ab', 'a-',
       'ab', 'a-', '--', '--', 'b-', 'ab', 'ab', 'ab', 'ab', 'b-', 'ab',
       '--', 'ab', 'a-', 'ab', 'ab', 'ab', 'ab', '--', 'ab', 'ab', 'ab',
       'ab', 'ab']



rec_flag = 1
trials = len(trial_type)
if rec_flag ==1:
    #ser=serial.Serial("COM13", baudrate=9600) # optogenetics
    ser3=serial.Serial("COM5", baudrate=9600)
    
    #ser.write('3')
    #trials = 100
    
#create a window
win = visual.Window( [1920,1080], 
                        monitor="mymon", 
                        units="deg", 
                        screen = 2, 
                        winType = 'pyglet',
                        colorSpace ='rgb',
                        color=0,
                        allowGUI=False
                       )


temporal_freq = 0 # Hz
spatial_freq= 0.05 #c/deg
phase_advance= temporal_freq/60.0 # monitor refresh rate 60 Hz
angle_iteration=15
orientations_number= 12
duration = 0.2
frames = int(duration *60)


cycle0=9
cycle1=3
#create some stimuli
grating = visual.GratingStim(win, 
                            mask='circle',
                            tex = 'sin', 
                            size=300, 
                            pos=[0,0], 
                            #opacity = 1,
                            sf=spatial_freq, 
                            ori = angle_iteration*cycle0, 
                            phase = 0)

grating2 = visual.GratingStim(win, 
                            mask='circle',
                            tex = 'sin', 
                            size=300, 
                            #opacity = 0.5,
                            pos=[0,0], 
                            sf=spatial_freq, 
                            ori = angle_iteration*cycle1, 
                            phase = 0)
                            



win.flip()
core.wait(4.0)
if rec_flag ==1:
    #ser=serial.Serial("COM13", baudrate=9600) # optogenetics
  
    ser3.write('3')


for ii, val in enumerate(trial_type[:]):

    print 'TTL signal received',ii, val
    if rec_flag ==1:
        
        ser3.write('1')
        #ser.write('1')
    core.wait(0.5) #units in seconds
    # learning stage
    if val == 'ab':
        for frameN in range(frames):
            grating.draw()
            win.flip()     
           
        win.flip() 
        core.wait(0.3)#0.25, 0.125, 0.0625
        for frameN in range(frames):
            grating2.draw()
            win.flip()     
        win.flip() 

    elif val == 'a-':
        for frameN in range(frames):
            grating.draw()
            win.flip()     
        win.flip() 
        
        core.wait(0.5)#0.25, 0.125, 0.0625
        

      
    elif val == 'b-':
        for frameN in range(frames):
            grating2.draw()
            win.flip()     
        win.flip() 
        
        core.wait(0.5) #0.25, 0.125, 0.0625
        
 
    elif val == '--':
        
        core.wait(0.7) #0.25, 0.125, 0.0625
        

    core.wait(2)
win.close()

 