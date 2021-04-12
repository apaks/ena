
#rec length 13 min, set Arduino to 60 000 ms, each trial 1 min rec

from __future__ import division
from psychopy import visual, core #import some libraries from PsychoPy
import socket #for connecting to other programs
import datetime, time, sys, serial
import scipy
import numpy as np
import pandas as pd
from subprocess import Popen#NEW
import pickle


path = r"U:\Visual Stimulation\pak6\Vis Stim\RF mapping\example_sequence.pkl"
seq = pd.read_pickle(path)
scale = 12
# 12 pix in 1 degree for 17 cm distance and 1920x1080 res for screen width of 48 cm
probe_size = 48

rec_flag = 0
trials = 13
if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)
    

probes = seq['frames']

white_tex=np.ones((int(probe_size/scale),int(probe_size/scale)), dtype = int)
grey_tex = np.zeros((int(probe_size/scale),int(probe_size/scale)), dtype = int)    
black_tex=-white_tex
# Create a window
win_size=[1920/scale,1080/scale]
mywin = visual.Window(win_size,
            monitor="mymon", 
            units="pix", 
            fullscr=False,
            screen=1)
            
#stim=visual.Rect(mywin, 
#        width = probe_size, height = probe_size, 
#        fillColor='white', lineColor=None
#        )          
stim=visual.GratingStim(mywin, 
                    tex=black_tex, 
                    size = probe_size/scale,
                    units = 'pix'
                    )

if rec_flag==1:

    ser.write('3')
core.wait(4)

#clock = core.Clock()

for i in range(trials):
    stims_ls = []
  
    print i
    x = 0
    end = (i+1)*3600
 

    if i == 0:
        core.wait(2)
        x= 120
    elif i ==12:
        end = len(probes)
    start = i*3600+x
    #print start, end

    for idx, val in enumerate(probes[start:end]):
        times = idx+start
        
        if idx%15==0:
            probes_ls = []   
            if val[1]>0:
                for sqr in val[1]:
                    stim=visual.GratingStim(mywin, 
                        tex=black_tex, 
                        size = probe_size/scale,
                        units = 'pix'
                        )
                    
                        #print sqr
                        #vertices = boxCoordinates(sqr, probe_size*scale)
                        
                    stim.pos = ((sqr[1]-60)*12/scale, (sqr[0])/scale*12)
                        #stim.setVertices = vertices
                    if sqr[2] == 1:
                        stim.tex = white_tex
                    else:
                        stim.tex = grey_tex
                    
                    probes_ls.append(stim)
                stims_ls.append(probes_ls)   
            else:
                continue
        else:
            continue
                
    print 'probes', len(stims_ls)
    if rec_flag==1:
        ser.write('1')
    if i == 0:
        core.wait(2)
        
    t2 = time.time() -1e-9
    for idx_stim, val_stim in enumerate(stims_ls[:]):
        #print idx_stim, len(val_stim)
        for frames in range(15):
            for probe in val_stim:
                probe.draw()
          
            mywin.flip()
        mywin.getMovieFrame()
        mywin.saveMovieFrames(fileName='probes_{times}.bmp'.format(times=str(i*10000+idx_stim) )) 

    t1 = time.time()-1e-9
  
    print t1-t2
    
            #print 'grey scr'
    
    mywin.flip()
    core.wait(10)
   
 
#mywin.saveMovieFrames(fileName='probes_off.gif')
mywin.close()

core.quit()