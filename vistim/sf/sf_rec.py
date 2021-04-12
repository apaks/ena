# Alex Pak, 2017 present vis stim from .npy files, 16s record
from __future__ import division
import numpy as np
from psychopy import visual, event, filters, core
import scipy.misc
import serial
from random import randint
import datetime

rec_flag = 0

trials = 20
#path = r"C:\Users\Achub_Lab\Desktop\Vis Stim\sf experiment\bp_noise_all.npy"
path = r"U:\Visual Stimulation\pak6\Vis Stim\bp_noise_all.npy"

imgs = np.load(path)

sf = 4
sf2 = 2
# 0-4 in increaassing spatial frequency
#noise = np.random.random([512, 512])*2-1

if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)
    trials = 20

win = visual.Window([1920,1080], 
    monitor='mymon', screen=1,
    fullscr = True)
    
  
core.checkPygletDuringWait = False
stim = visual.ImageStim(win, 
    image = imgs[sf], # change this to sf stim 
    units="pix", 
    size=imgs[0].shape)
    
stim2 = visual.ImageStim(win, 
    image = imgs[sf2], # change this to sf stim 
    units="pix", 
    size=imgs[0].shape)

stim_duration = 0.2 # in sec
one_frame = 1/60.0
frames = int(60*stim_duration)

base_duration = 0.5
interval_duration = 0.2500

core.wait(4)
if rec_flag==1:

    ser.write('3')
    #ser2.write('3')
    
clock = core.Clock()

win.recordFrameIntervals = True
print 'Experiment starts at:', datetime.datetime.now().time()
for j in range(trials):
    clock.reset()
    print 'trial',j
    
    if rec_flag==1:
        ser.write('1')
        #ser2.write('1')
    core.wait(0.5)
 
    t1 = clock.getTime()

    
    for l in range(frames):
        
        stim.draw()
        win.flip()
        
    win.flip()
    t1_end = clock.getTime()
    core.wait(0.25)
    # 0.15 for in-phase
    t2 = clock.getTime()
    for l in range(frames):
        
        stim2.draw()
        win.flip()
        
    win.flip()
    t2_end = clock.getTime()
    print t1, t1_end-t1, t2-t1_end, t2_end-t2
    rint = randint(5,10)
    core.wait(rint)

#event.waitKeys()

