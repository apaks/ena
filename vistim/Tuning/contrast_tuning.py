
# Alex Pak, 2018
# prandomly present 5 contrasts, 20 trials
# total rec length 100 trials * 6 (max trial length) = 600 s = 10 min

from psychopy import visual, core #import some libraries from PsychoPy
import sys
import datetime
import time
from random import randint
import serial

rec_flag = 1
if rec_flag == 1:
    ser=serial.Serial("COM5", baudrate=9600)
#create a window

win = visual.Window( [1920,1080], 
                        monitor="mymon", 
                        units="pix", 
                        fullscr=True,
                        screen = 1, 
                        winType = 'pyglet',
                        colorSpace ='rgb',
                        color=0,
                       )

duration = 0.5
frames = int(duration * 60)
temporal_freq = 2 # Hz
spatial_freq=0.04
phase_advance= temporal_freq/60.0 # monitor refresh rate 60 Hz
angle_iteration = 30

contrast_seq = [1, 0.25, 0.125, 1, 0.0625, 1, 1, 0.5, 0.0625, 0.125, 0.5, 
0.125, 0.5, 0.5, 0.125, 0.125, 0.5, 0.25, 0.5, 0.0625, 1, 0.0625, 0.5, 1, 
1, 0.125, 1, 0.125, 0.125, 0.25, 0.0625, 0.0625, 0.125, 0.5, 0.125, 0.5, 
0.0625, 1, 1, 0.25, 0.25, 1, 1, 0.25, 0.125, 1, 0.25, 0.5, 0.0625, 0.5, 
0.125, 0.0625, 0.25, 0.0625, 0.25, 0.5, 0.25, 0.5, 0.125, 0.125, 1, 1, 
0.5, 0.5, 0.125, 1, 0.25, 0.0625, 0.25, 0.25, 1, 1, 0.25, 0.5, 0.5, 0.125, 
1, 0.125, 0.0625, 0.125, 0.25, 0.0625, 0.25, 0.0625, 0.0625, 0.0625, 0.5, 
0.125, 0.25, 0.5, 0.0625, 0.25, 0.5, 0.0625, 0.25, 1, 0.0625, 0.0625, 0.25, 0.125]



#create some stimuli
grating = visual.GratingStim(win, 
                            mask='circle',
                            tex = 'sin', 
                            size=300, 
                            units = 'deg',
                            pos=[0,0], 
                            sf=spatial_freq, 
                            ori = 0, 
                            opacity = contrast_seq[0],
                            phase = 0)


win.flip()
core.wait(4.0)
if rec_flag == 1:
    ser.write('3')

for idx, val in enumerate(contrast_seq): #number of trials
    
    if rec_flag == 1:
        ser.write('1')
    core.wait(0.3) #units in seconds
                
    for frameN in range(frames):
        #grating.setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
        grating.draw()
        win.flip()   
            
    win.flip() 
    
    grating.setOpacity(contrast_seq[idx+1])
#    grating.setPhase(0)

    x = randint(3,5)
    # print x
    core.wait(x)
            

        


