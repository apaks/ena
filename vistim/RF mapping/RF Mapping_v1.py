#V1 receptive field mapping (0.4+0.3+0.3 per presentation)
# Arduino 1s
from __future__ import division
from psychopy import visual, core #import some libraries from PsychoPy
import socket #for connecting to other programs
import datetime
import time
import serial
import scipy
import sys
import numpy as np

from subprocess import Popen#NEW
#script = r"C:\Users\Achub_Lab\Desktop\Vis Stim\12 Drifting\Save_video_sockets_12-Drifting.py"
# run script
#theproc = Popen(["python", script])
rec_flag = 0

connected=False

if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)
    
    

#ser1=serial.Serial("COM7", baudrate=9600)

# Create a window
win_size=[1920,1080]
mywin = visual.Window(win_size,
            #monitor="mymon", 
            units="deg", 
            fullscr=False,
            screen=2)

# Create some stimuli
# Stimulation parameters
grid_dimension=[4,4]
a,b=grid_dimension
x,y=(int(min(win_size)/a), int(min(win_size)/b)) # size of the stimulus 
stim_duration=0.3 # when the duration*60 does not equal to an integar, the stimulus presentation line needs to be changed
num_stimtype=2 #white and black stim
num_pres=a*b*num_stimtype
num_trials=10
isi=0.3 #inter stim interval


# White or Black Texture
white_tex=np.ones((x,y),dtype=int)
black_tex=-white_tex


# Stimulus Position List
positions=[]
position = [(x-min(win_size))/2,(min(win_size)-y)/2] # upper left corner block position
for i in range(a):
    for ii in range(b):
        positions.append(tuple(position))
        position[0]+=x
        ii+=1
    position[0]+=-a*x
    position[1]+=-y
#print positions
# Stimullus Type List
stim_idx=range(num_stimtype)


# Pseudorandom order of white or black stimulus
prand_stim=[1, 0, 1, 0, 0, 0, 1, 1, 
             1, 0, 0, 0, 1, 1, 0, 1, 
             0, 1, 0, 1, 0, 1, 1, 0, 
             1, 1, 0, 1, 1, 0, 0, 0] # 0 is white, 1 is black # new


prand_pos=[[135, -135], [135, 405], [-405, 135], [135, -405], [-405, 135], [-405, -405], [-135, -405], [135, -405], [-405, -135], [-405, 405], [135, 135], [405, -405], [135, 135], [405, -135], [-135, -135], [405, 135], [-135, 135], [-405, 405], [405, 135], [-135, -135], [-405, -135], [405, -405], [405, 405], [-135, -405], [135, 405], [-135, 135], [-135, 405], [-405, -405], [-135, 405], [405, -135], [405, 405], [135, -135]]
[ 135. -135.]


mywin.update()
core.wait (4.0)

if rec_flag==1:
    ser.write('3')
#Initialization signal for arduino to open serial port for openephys DataAcq


# Draw stimuli
for i in range(num_trials):
   
    stim=visual.GratingStim(mywin, tex=black_tex, size=(x,y), units='pix',pos=prand_pos[0])
    for n in range(num_pres):
        #clientsocket.send('Hi there!') #This message triggers opening of video cap & rec start
        if prand_stim[n] == 0:
            stim.tex=white_tex
        else:
            stim.tex=black_tex
        stim.pos=prand_pos[n]
        print 'Sent', i, n
#        DataValue=ser.read()
#        buff = connection.recv(32)
        
        
        print 'Cycle starts at:', datetime.datetime.now().time()
        
        
            #print 'TTL signal received'
        if rec_flag==1:
            ser.write('1')
        core.wait(0.4) #units in seconds

        for frameN in range(int(stim_duration*60)):
            stim.draw()
            mywin.flip()
            
        mywin.flip()
        core.wait(3.0)
        #print 'Cycle ends at: ', datetime.datetime.now().time(), '\n'
        
        

    

#close the window
mywin.close()

