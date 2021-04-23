
# Alex Pak, 2018
# prandomly present 12 directions, 6 orientations
# total rec length 180 trials * 6 (max trial length) = 1080 s = 18 min

from psychopy import visual, core #import some libraries from PsychoPy
import sys
import datetime
import time
from random import randint
import serial
import numpy as np

rec_flag = 0
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

duration = 1
frames = int(duration * 60)
temporal_freq = 2 # Hz
spatial_freq=0.04
phase_advance= temporal_freq/60.0 # monitor refresh rate 60 Hz

angle_iteration = 30 # 30 for 12, 45 for 8 directions

dir12_seq = [10, 7, 3, 2, 4, 8, 9, 5, 7, 3, 4, 8, 3, 2, 1, 8, 0, 4, 9, 11, 
10, 9, 1, 11, 4, 0, 7, 1, 2, 8, 2, 9, 11, 9, 6, 5, 10, 4, 9, 0, 7, 11, 9, 
5, 9, 10, 11, 6, 8, 9, 5, 4, 2, 8, 11, 2, 10, 3, 5, 1, 7, 0, 4, 9, 1, 5, 
11, 3, 5, 10, 1, 2, 9, 6, 2, 2, 11, 5, 10, 7, 3, 7, 4, 6, 8, 4, 1, 8, 0, 
11, 0, 6, 2, 11, 1, 10, 3, 8, 3, 1, 2, 10, 5, 3, 11, 1, 7, 3, 4, 7, 8, 4, 6, 
7, 11, 7, 0, 8, 6, 10, 4, 5, 7, 2, 10, 3, 5, 9, 8, 6, 3, 2, 0, 11, 0, 6, 10, 
0, 7, 4, 5, 0, 10, 6, 8, 10, 3, 11, 9, 0, 5, 1, 3, 7, 0, 6, 9, 1, 6, 10, 5, 
6, 11, 7, 0, 5, 1, 4, 1, 6, 8, 2, 9, 2, 8, 3, 0, 4, 6, 1]

dir8_seq = np.array([2, 0, 7, 5, 6, 3, 3, 1, 4, 5, 4, 7, 4, 7, 5, 2, 2, 2, 2, 1, 1, 7,
       5, 3, 1, 1, 3, 4, 2, 3, 6, 6, 0, 5, 1, 2, 7, 6, 5, 3, 5, 4, 5, 6,
       5, 4, 4, 6, 6, 4, 0, 2, 7, 7, 0, 4, 5, 1, 2, 4, 3, 3, 4, 5, 7, 5,
       4, 7, 2, 4, 5, 7, 0, 1, 2, 2, 3, 6, 1, 3, 5, 1, 5, 1, 2, 6, 0, 1,
       7, 1, 0, 6, 7, 6, 5, 3, 3, 2, 5, 7, 0, 4, 3, 0, 1, 4, 1, 3, 5, 2,
       0, 1, 6, 0, 5, 7, 1, 7, 3, 0, 6, 7, 0, 2, 5, 2, 3, 7, 4, 3, 3, 6,
       3, 1, 2, 1, 5, 7, 6, 0, 3, 3, 0, 4, 0, 7, 1, 2, 0, 3, 0, 0, 6, 5,
       2, 5, 4, 2, 7, 0, 1, 3, 2, 7, 6, 6, 1, 0, 1, 5, 6, 0, 3, 2, 6, 4,
       7, 0, 7, 4, 6, 5, 4, 1, 6, 2, 4, 4, 2, 4, 7, 6, 0, 4, 3, 1, 6, 6,
       0, 7])
#create some stimuli
exp = dir12_seq
grating = visual.GratingStim(win, 
                            mask='gauss',
                            tex = 'sin', 
                            size=200, 
                            units = 'deg',
                            pos=[0,0], 
                            sf=spatial_freq, 
                            ori = angle_iteration*exp[0], 
                            phase = 0)


win.flip()
core.wait(4.0)
if rec_flag == 1:
    ser.write('3')

for idx, val in enumerate(exp): #number of trials
    if idx%40==0:
        print idx, val*30

    if rec_flag == 1:
        ser.write('1')
#    core.wait(0.3) #units in seconds
                
    for frameN in range(frames):
        grating.setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
        grating.draw()
        win.flip()   

        win.getMovieFrame()
    win.flip() 
    win.getMovieFrame()
    win.saveMovieFrames(fileName='grating.mp4')
    break
    grating.setOri(angle_iteration*exp[idx+1])
    grating.setPhase(0)

    x = randint(3,4)
    # print x
    core.wait(x)
            

        


