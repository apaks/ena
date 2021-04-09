# Alex Pak, 2017 present vis stim from .npy files, 8s record, 1s base - 5s (5stims) - 2s 
from __future__ import division
import numpy as np
from psychopy import visual, event, filters, core
import scipy.misc
import serial
from random import randint
import datetime

rec_flag = 0

trials = 20

#path = r"U:\Visual Stimulation\pak6\Vis Stim\natural_images\nat_mov_lp03.npy"
path = r"U:\Visual Stimulation\pak6\Vis Stim\natural_images\nat_mov_hp05_scrambled.npy"
imgs = np.load(path)

# 0-4 in increaassing spatial frequency
#noise = np.random.random([512, 512])*2-1

if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)
    trials = 20

win = visual.Window([1920,1080], 
    monitor='mymon', screen=2,
    fullscr = False)
    
stims = []
core.checkPygletDuringWait = False
for i in range(5):
    stims.append(visual.ImageStim(win, 
    image = imgs[i], # change this to sf stim 
    units="pix", 
    size= (imgs[0].shape[1], imgs[0].shape[0])))
    
stim_duration = 1 # in sec
one_frame = 1/60.0
frames = int(60*stim_duration)


core.wait(4)
if rec_flag==1:

    ser.write('3')
    #ser2.write('3')
    
clock = core.Clock()

print 'Experiment starts at:', datetime.datetime.now().time()
for j in range(trials):
    #clock.reset()
    print 'trial',j
    
    if rec_flag==1:
        ser.write('1')
        #ser2.write('1')
    core.wait(1)
    for idx in range(5):
        
        for l in range(frames):
            
            stims[idx].draw()
            win.flip()
            
        win.flip()
    rint = randint(5,10)
    core.wait(rint)

#event.waitKeys()

