
from __future__ import division
from psychopy import visual, core #import some libraries from PsychoPy
import socket #for connecting to other programs
import datetime, time, sys, serial
import scipy
import numpy as np
import pandas as pd
from subprocess import Popen#NEW
import pickle


def boxCoordinates(centre, size):

    size = size / 2    
    
    box_vertices = [ \
    [centre[0] - size, centre[1] - size - 60], \
    [centre[0] - size, centre[1] + size - 60], \
    [centre[0] + size, centre[1] + size - 60], \
    [centre[0] + size, centre[1] - size - 60] ]
    
    return box_vertices
    
path = r"U:\Visual Stimulation\pak6\Vis Stim\RF mapping\example_sequence.pkl"
seq = pd.read_pickle(path)
scale = 1
# 12 pix in 1 degree for 17 cm distance and 1920x1080 res f
# 0.0801190655761 degrees correspond to a single pixel
# mon_width_cm = 52 #enter your monitors width in cm
# mon_height_cm = 32 #enter your monitors height in cm
probe_size =  48.0
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
            fullscr=True,
            screen=2)
            
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

clock = core.Clock()
for i in range(trials):
    clock.reset()
    print i
    x = 0
    end = (i+1)*3600
    error = []
    if rec_flag==1:
        ser.write('1')
    if i == 0:
        core.wait(2)
        x= 120
    elif i ==12:
        end = len(probes)
    start = i*3600+x
    #print start, end
    error = []
    for idx, val in enumerate(probes[start:end]):
        times = idx+start
        
        if val[1] > 0:
            
            for sqr in val[1]:
                #print sqr
                #vertices = boxCoordinates(sqr, probe_size*scale)
                
                stim.pos = ((sqr[1]-60)*12/scale, (sqr[0])/scale*12)
                #stim.setVertices = vertices
                if sqr[2] == 1:
                    stim.tex = white_tex
                else:
                    stim.tex = black_tex
                    
                stim.draw()
            
            mywin.flip()
 
            if idx%15==0:
                t1 = clock.getTime()  
                print t1*(i+1)-times/60
            
                mywin.getMovieFrame()
                mywin.saveMovieFrames(fileName='probes_{times}.bmp'.format(times=str(times) ))  
                
        else:
            break
            #print 'grey scr'
                
 
    print error       
    mywin.flip()

    core.wait(5)
   
 
#mywin.saveMovieFrames(fileName='probes_off.gif')
mywin.close()

core.quit()