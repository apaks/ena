
# Alex Pak, 2016
# trial duration 1.5s

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
    'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'aa', 'ab', 'ab', 'ba', 'aa',
       'aa', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'bb',
       'ab', 'ab', 'ab', 'ba', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab',
       'ba', 'bb', 'ab', 'bb', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab',
       'ab', 'ab', 'ab', 'ab', 'ba', 'ab', 'ab', 'ab', 'ab', 'ba', 'bb',
       'aa', 'ab', 'aa', 'ab', 'ab', 'ab', 'bb', 'ab', 'aa', 'ab', 'ab',
       'ab', 'ab', 'aa', 'ab', 'bb', 'ab', 'aa', 'bb', 'ba', 'ab', 'ab',
       'ab', 'ab', 'ab', 'ab', 'ba', 'ab', 'bb', 'ab', 'ab', 'ba', 'ab',
       'aa', 'bb', 'aa', 'ab', 'bb', 'ab', 'ab', 'bb', 'ab', 'ab', 'ab',
       'ab', 'ab', 'ab', 'ab', 'ab', 'ab', 'aa', 'ab', 'ab', 'aa', 'ab',
       'ab', 'ab', 'ab', 'ab', 'ba', 'ab', 'ba', 'ab', 'ab', 'ab', 'ab',
       'ab', 'ab', 'ab', 'ba', 'ab', 'ab', 'ab', 'ab', 'ab', 'bb', 'ab',
       'ab', 'ab', 'ba', 'ab', 'aa', 'ab', 'ab', 'ba', 'aa', 'ba', 'ba',
       'ab', 'ab', 'ab', 'ba', 'ab', 'ba', 'aa', 'ba', 'ab', 'ab', 'ab',
       'ab', 'ab', 'bb', 'ab', 'bb', 'ab', 'ab', 'ab', 'ab', 'ab', 'ab',
       'ab', 'aa', 'ab', 'ab', 'ba', 'bb', 'ab', 'ab', 'bb', 'ab', 'ab',
       'ba', 'bb', 'ab', 'aa', 'ab', 'ab', 'bb', 'aa', 'ab', 'ab', 'ab',
       'ab', 'ab', 'aa', 'ab', 'ab', 'ab', 'bb', 'ab', 'ab', 'ab', 'ab',
       'aa', 'bb']


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

    elif val == 'aa':
        for frameN in range(frames):
            grating.draw()
            win.flip()     
        win.flip() 
        
        core.wait(0.3)#0.25, 0.125, 0.0625
        
        for frameN in range(frames):
            grating.draw()
            win.flip()     
           
        win.flip() 
      
    elif val == 'ba':
        for frameN in range(frames):
            grating2.draw()
            win.flip()     
        win.flip() 
        
        core.wait(0.3) #0.25, 0.125, 0.0625
        
        for frameN in range(frames):
            grating.draw()
            win.flip()     
           
        win.flip() 
 
    elif val == 'bb':
        for frameN in range(frames):
            grating2.draw()
            win.flip()     
        win.flip() 
        
        core.wait(0.3) #0.25, 0.125, 0.0625
        
        for frameN in range(frames):
            grating2.draw()
            win.flip()     
           
        win.flip() 
          
    x = randint(10,20)  
    if ii<100:
        x = 2
    core.wait(x)
Win.close()

 