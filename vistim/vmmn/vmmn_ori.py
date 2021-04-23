# vMMN for mouse autism models, Alex Pak, 2017
# 300 trials, 1s rec 0.5-0.7(stim)-0.3, 1s iti, 10 min rec
# deviant stim = 10%

from __future__ import division
from psychopy import visual, core, event
import numpy as np
import serial
from random import randint

rec_flag = 0

if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)
  
    
myWin = visual.Window( [1920,1080], 
                        monitor="testMonitor", 
                        #units="pix", 
                        screen=2, 
                        winType = 'pyglet',
                        colorSpace ='rgb',
                        fullscr = 'True',
                        #color=0.18,
                       )

trials = 300

lin_prob_oddball = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
3, 3, 3, 3, 3, 3,
 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
 3, 3, 3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3,
 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
 3, 3, 9, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 9, 3, 3,
 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 3,
 3, 3, 9, 3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3,
 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3,
 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 3, 3,
 9, 3, 3, 3, 9, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3,
 3, 3, 3, 9, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3,
 3, 3, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 9, 3,
 3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 9]

rev_lin_prob_oddball = [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
9, 9, 9, 9, 9, 9,
 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
 9, 9, 9, 9, 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9,
 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
 9, 9, 3, 9, 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
 3, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9, 3, 9, 9,
 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9, 9,
 9, 9, 3, 9, 9, 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9, 9, 9, 3, 9, 9, 9,
 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9,
 9, 9, 9, 9, 3, 9, 9, 9, 9, 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9, 9, 9,
 3, 9, 9, 9, 3, 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9,
 9, 9, 9, 3, 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9, 9, 9, 3, 9, 9, 9, 9,
 9, 9, 3, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9, 3, 9,
 9, 9, 9, 9, 9, 9, 9, 3, 9, 9, 9, 9, 9, 3]

control = [8, 12, 4, 9, 4, 10, 12, 8, 2, 10, 4, 9, 9, 4, 3, 2, 10, 2, 4, 10, 8, 4, 10, 10, 12, 3, 10, 2, 3, 10, 9, 2, 8, 6, 2, 10, 12, 9, 9, 2, 6, 4, 10, 12, 12, 12, 3, 6, 4, 4, 12, 6, 3, 6, 4, 10, 3, 3, 6, 3, 8, 3, 12, 6, 9, 12, 10, 3, 8, 8, 12, 6, 9, 9, 3, 10, 2, 6, 10, 4, 12, 9, 2, 10, 9, 4, 3, 2, 9, 12, 2, 8, 8, 8, 12, 8, 9, 2, 8, 6, 10, 8, 10, 2, 8, 9, 8, 9, 9, 3, 4, 2, 8, 4, 2, 3, 4, 8, 12, 4, 6, 10, 12, 9, 8, 8, 3, 2, 6, 6, 3, 10, 4, 10, 2, 9, 10, 6, 3, 10, 8, 12, 9, 3, 8, 4, 2, 8, 4, 8, 12, 4, 6, 12, 10, 10, 9, 4, 12, 10, 3, 6, 2, 9, 4, 12, 2, 12, 3, 2, 6, 9, 6, 8, 2, 4, 3, 2, 6, 9, 2, 8, 12, 6, 10, 6, 9, 6, 6, 8, 2, 4, 9, 3, 9, 6, 12, 10, 2, 12, 3, 8, 6, 3, 3, 12, 3, 12, 6, 9, 6, 12, 3, 8, 4, 9, 12, 2, 2, 2, 9, 10, 12, 8, 4, 4, 6, 10, 10, 6, 9, 8, 3, 3, 4, 4, 3, 4, 2, 6]


loc_omission = [3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 
0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 
3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 
3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 
3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 
3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 
3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 
3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0]

glob_omission = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3,
3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 0, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3,
3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0,
3, 3, 0, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 0, 3, 3, 3, 
3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 
3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 0, 3, 3, 3, 
3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 0, 3, 3, 3, 
3, 3, 3, 3, 0, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3]



trial_type = lin_prob_oddball

stim_duration = 0.5 # in sec
one_frame = 1/60.0
frames = int(60*stim_duration)
phase_advance = 0.05
dir_step = 15                       
stim1 = visual.GratingStim(myWin, 
                            mask='circle', 
                            #color=[1.0,1.0,1.0],
                            fullscr=True,
                            opacity = 0.5, 
                            tex = 'sqr',
                            units = 'deg',
                            size=1000, 
                            sf=(0.04,0), 
                            ori = dir_step*trial_type[0], 
                            autoLog=False)
#this stim changes too much for autologging to be useful 

core.checkPygletDuringWait = False

core.wait(4)
if rec_flag==1:

    ser.write('3')
    #ser2.write('3')
clock = core.Clock()
for idx, val in enumerate(trial_type):
#    clock.reset()
    # print 'trial', idx
    iti = np.random.uniform(0.7, 1.2)
    stim1.ori = dir_step*val
    if 'omission' in trial_type:
        iti = 1
        if value == 0:
            stim1.opacity = 0
            
    if rec_flag==1:
        ser.write('1')
        #ser2.write('1')
    core.wait(0.3)
 
#    t1 = clock.getTime()

    #print t1
    for l in range(frames):
        
        stim1.draw()
        myWin.flip()
    myWin.flip()
#    stim1.setPhase(phase_advance, '+')
#    stim1.contrast = 1
    #t2_end = clock.getTime()
    #print t1, t1_end-t1, t2-t1_end, t2_end-t2
    stim1.opacity = 0.5
    core.wait(iti)                       
                       
                       
                       
                       
                       
                       