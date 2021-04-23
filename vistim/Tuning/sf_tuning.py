# Alex Pak, 2017 present vis stim from .npy files,  record
# sf - 0.01, 0.02, 0.04, 0.08, 0.16, 0.32 cyc/deg
# Arduino set 1s each trial
# total time for rec = 5*120 = 600 s

from __future__ import division
import numpy as np
from psychopy import visual, event, filters, core
import scipy.misc
import serial
from random import randint
import datetime

rec_flag = 1

path = r"U:\Visual Stimulation\pak6\Vis Stim\Tuning\sf_tuning_01_32.npy"
imgs = np.load(path)

sf_seq = [2, 0, 0, 4, 3, 3, 0, 4, 4, 3, 2, 5, 3, 2, 0, 4, 1, 0, 5, 2, 0, 
1, 0, 1, 3, 5, 2, 5, 1, 2, 0, 5, 2, 3, 5, 1, 0, 4, 3, 2, 5, 5, 3, 5, 
2, 0, 3, 3, 0, 3, 4, 5, 4, 1, 4, 0, 1, 5, 4, 1, 5, 3, 3, 5, 3, 3, 2, 
3, 2, 1, 1, 5, 1, 4, 1, 2, 3, 2, 4, 2, 1, 0, 5, 5, 2, 2, 4, 1, 4, 1, 
3, 1, 0, 4, 4, 4, 4, 0, 5, 4, 4, 0, 3, 5, 5, 2, 1, 3, 4, 1, 5, 0, 2, 
2, 0, 0, 0, 1, 2, 1]

if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)

win = visual.Window( [1920,1080], 
                        monitor="mymon", 
                        units="pix", 
                        screen = 2, 
                        winType = 'pyglet',
                        colorSpace ='rgb',
                        color=0,
                       )
    
core.checkPygletDuringWait = False
stim = visual.ImageStim(win, 
    image = imgs[sf_seq[0]], # change this to sf stim 
    units="pix", 
    size=(imgs[0].shape[1], imgs[0].shape[0]))
    
stim_duration = 0.5 # in sec
one_frame = 1/60.0
tf = 0
frames = int(60*stim_duration)

core.wait(4)
if rec_flag==1:
    ser.write('3')
    #ser2.write('3')
   
win.recordFrameIntervals = True
print 'Experiment starts at:', datetime.datetime.now().time()
for idx, val in enumerate(sf_seq):
    print 'trial', idx
    if rec_flag==1:
        ser.write('1')
        #ser2.write('1')
    core.wait(0.3)
   
    for l in range(frames):
        stim.draw()
        win.flip()
        
    win.flip()
    stim.image = imgs[sf_seq[idx+1]]
    rint = randint(3,5)
    core.wait(rint)

#event.waitKeys()

