# Alex Pak, 2017 present vis stim from .npy files, 16s record
from __future__ import division
import numpy as np
from psychopy import visual, event, filters, core
import scipy.misc
import serial
from random import randint
import datetime

rec_flag = 0

trials = 200
#path = r"C:\Users\Achub_Lab\Desktop\Vis Stim\sf experiment\bp_noise_all.npy"
path = r"U:\Visual Stimulation\pak6\Vis Stim\tf_exp\tf_stim_bp_noise_sf42.npy"
imgs = np.load(path)

sf = 2

# 0-4 in increaassing spatial frequency
#noise = np.random.random([512, 512])*2-1

if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)
    trials = 20

win = visual.Window([1920,1080], 
    monitor='mymon', screen=2,
    fullscr = True)
    
  
core.checkPygletDuringWait = False


clock = core.Clock()

test_img = imgs
framerate=60 # Hz
duration = 0.6 # in sec
frame_num = int(duration*framerate)

temporal_frequency = 1

tf_stim = np.zeros((frame_num,test_img.shape[0], test_img.shape[1] ), dtype='float32')

#sin_drift_noise=[]
#sin_drift_noise.append(test_img)
starting_phase=np.arcsin(test_img)
phase_shift=2*np.pi/framerate

for i in range(frame_num):
    
    new_frame=np.sin(temporal_frequency*(phase_shift)+starting_phase)
    tf_stim[i] = new_frame
    starting_phase = temporal_frequency*(phase_shift)+starting_phase 
    #sin_drift_noise.append(new_frame)
    
#win.recordFrameIntervals = True
ls = []
for i in range(frame_num):
    img = visual.ImageStim(
        win=win,
        colorSpace = 'rgb',
        image = tf_stim[i],
        units="pix",
        #mask = 'gauss',
        size = np.shape(tf_stim[0])
        
    )
    ls.append(img)
core.wait(4)
if rec_flag==1:

    ser.write('3')
    #ser2.write('3')
    

print 'Experiment starts at:', datetime.datetime.now().time()
for j in range(trials):
    #clock.reset()
    print 'trial',j
    
    if rec_flag==1:
        ser.write('1')
        #ser2.write('1')
    core.wait(0.5)
 
    

    t1 = clock.getTime()
    for j in range(frame_num):
        
        #img.image = tf_stim[j]
        
        #print j, tf_stim[j][0][0]
        ls[j].draw()
        win.flip()
        
    win.flip()
    t1_end = clock.getTime()
#    core.wait(0.25)
#    t2 = clock.getTime()
#    for l in range(frames):
#        
#        stim2.draw()
#        win.flip()
#        
#    win.flip()
#    t2_end = clock.getTime()
    print t1_end-t1
    rint = randint(7,10)
    core.wait(rint)

#event.waitKeys()

