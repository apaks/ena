# visual chirp

from __future__ import division
from psychopy import visual, core #import some libraries from PsychoPy
import socket #for connecting to other programs
import datetime, time, sys, serial
import scipy.signal as sg
import numpy as np

rec_flag = 1
if rec_flag ==1:
    #ser=serial.Serial("COM13", baudrate=9600) # optogenetics
    ser3=serial.Serial("COM6", baudrate=9600)

t = np.linspace(0.5, 6, 361)
w = sg.chirp(t, f0=0.5, f1=10, t1=6, method='linear')

win_size=[1920,1080]
mywin = visual.Window( size = [1920,1080],
            monitor="mymon", 
            units="pix", 
            fullscr=True,
            screen=2)
            
            
img = visual.ImageStim(
    win=mywin,
    
    units="pix",
    #mask = 'gauss',
    size = win_size
    #mask = 'gauss' 
)

grid_dimension=[4,4]
a,b=grid_dimension
x,y=(int(min(win_size)/a), int(min(win_size)/b))
print x
#tex = np.random.randint(2, size=[x,y], dtype = 'int')

def build_checkerboard(w, h):
      re = np.r_[ w*[1] ]              # even-numbered rows
      re = np.repeat(re, w).reshape(-1,w)
      ro = np.r_[ w*[-1]]              # odd-numbered rows
      ro = np.repeat(ro, w).reshape(-1, w)
      tex =  np.row_stack(h*(re, ro))
      tex = np.hstack((tex, np.flipud(tex)))
      return np.tile(tex, h)
      
tex = build_checkerboard(1, 4)

stim = visual.GratingStim(mywin, 
                tex=tex, 
                size=1600, 
                units='pix')
                
temporal_frequency = 50
dur = 6 # in sec
starting_phase=np.arcsin(tex)
#phase_shift = np.arcsin(w)
framerate = 60
frames = int(dur*framerate)
#phase_shift = 2*np.pi/framerate
#
tf_stim = np.zeros((frames,tex.shape[0], tex.shape[1] ), dtype='float32')
#for i in range(frames):
#    new_frame=np.sin(temporal_frequency*(phase_shift)+starting_phase)
#    tf_stim[i] = new_frame
#    starting_phase = temporal_frequency*(phase_shift)+starting_phase 
ls_stims = []

for i in range(frames):
    
    new_frame = np.sin(np.arcsin(w[i]) + starting_phase)
    tf_stim[i] = new_frame
    starting_phase = np.arcsin(w[i]) + starting_phase
    
if rec_flag ==1:
    #ser=serial.Serial("COM13", baudrate=9600) # optogenetics
  
    ser3.write('3')

for i in range(frames):
    stim = visual.GratingStim(mywin, 
                tex=tf_stim[i], 
                size=1600, 
                units='pix')
    ls_stims.append(stim)

for i in range(20):
    print i
    if rec_flag ==1:
        ser3.write('1')
    core.wait(1)
    for j in range(frames):

        img.color = w[j]
        img.draw()

#        ls_stims[j].draw()
        mywin.flip()
#        mywin.getMovieFrame()
        
        #mywin.saveMovieFrames(fileName='probes_{times}.bmp'.format(times=str(idx) ))  
    mywin.flip()
    core.wait(7)
#mywin.saveMovieFrames(fileName='chirp_checkerboard.gif') 
mywin.close()