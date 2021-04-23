
# Alex Pak, 2018
from __future__ import division
from psychopy import visual, core #import some libraries from PsychoPy
import datetime
import sys
import socket #for connecting to other programs
import serial, pickle
from random import randint
from scipy import random 
import numpy as np
from subprocess import Popen
connected=False

ppl_flag = 1
ephys_flag = 0
speed_flag = 1

if ephys_flag == 1:
    #ser=serial.Serial("COM13", baudrate=9600) # optogenetics
    ser_ephys = serial.Serial("COM5", baudrate=9600)
    
if speed_flag == 1:
    ser_speed = serial.Serial("COM8", baudrate=9600) 
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename =  'speed_' + str(date) + '.pkl'
    print filename
    output = open(filename, 'wb')
    ser_speed.write('3')

if ppl_flag == 1:
    script = r"C:\Sam Visual Stim\Pak_vMMN_new\pupil_socket.py"
    theproc = Popen(["python", script])
    core.wait(0.5)
    
glob_oddball = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 
1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 
1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 
1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 
1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 
1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1]


#create a window
win = visual.Window( [1920,1080], 
                        monitor="mymon", 
                        units="deg", 
                        fullscr=True,
                        screen = 2, 
                        winType = 'pyglet',
                        colorSpace ='rgb',
                        color=0,
                        allowGUI=False
                       )


temporal_freq = 2 # Hz
spatial_freq= 0.05 #c/deg
phase_advance= temporal_freq/60.0 # monitor refresh rate 60 Hz
angle_iteration = 15
orientations_number=12
duration = 0.5
frames = int(duration *60)

cycle0=1

#create some stimuli
grating = visual.GratingStim(win, 
                            mask='circle',
                            tex = 'sin', 
                            size=300, 
                            pos=[0,0], 
                            #opacity = 1,
                            sf=spatial_freq, 
                            ori = angle_iteration*cycle0, 
                            phase = 0)


def make_gray_checkerboard(idx):                         
    noiseTexture = random.rand(16,16)*2.0-1.0
    speed = 256
    myPatch = visual.GratingStim(win, tex=noiseTexture, 
        size= 2500, units='pix',
        interpolate=False, mask='circle', ori = idx*angle_iteration,
        autoLog=False)#this stim changes too much for autologging to be useful
        #add ori=30 to set orientation.  make phase to be 180 without ori, then set ori
    return myPatch

if ppl_flag == 1:

    #Sockets client
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8090))#8089

    print 'Stimuli listen ready\n';
    sys.stdout.flush();

    #Sockets server
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 8091)) #8089
    serversocket.listen(5) # become a server socket, maximum 5 connections
    connection, address = serversocket.accept()


win.flip()
core.wait(4.0)
if ephys_flag ==1:
    #ser=serial.Serial("COM13", baudrate=9600) # optogenetics
    ser_ephys.write('3')

for idx, val in enumerate(glob_oddball[:]):
    print idx, val
#    val = 2
    
    if ppl_flag == 1:  
        clientsocket.send('Hi there!') #This message triggers opening of video cap & rec start
   
        buff = connection.recv(32)
 
    if val == 2:
        ori = randint(0,12)
        myPatch = make_gray_checkerboard(ori) 
        
    if len(buff) > 0:
        if speed_flag ==1:
            ser_speed.write('1') 
        if ephys_flag ==1:
            
            ser_ephys.write('1')
            #ser.write('1')
        core.wait(0.5) #units in seconds
        if val ==1:
            for frameN in range(frames):
                #grating.setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
                grating.draw()
                win.flip()     
            grating.setPhase(0)    
            win.flip() 
        else:
            for frameN in range(frames):
                #myPatch.phase += (1 / speed, 0 / speed)  # increment by (1, 0) pixels per frame
                myPatch.draw()
                win.flip()
            win.flip()

        core.wait(4)
        if speed_flag ==1:
            ser_speed.write('2')
            x2 = ser_speed.readline()
#            print x2
            try:
                pickle.dump(x2, output)
            except:
                print ('data not written')
        core.wait(0.5)
output.close()
clientsocket.send('Finished')
win.close()


 