
# Alex Pak, 2016
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

ppl_flag = 0
rec_flag = 0
speed_flag = 0
opto_flag = 0
trials = 20

if opto_flag==1:
    ser_opto = serial.Serial("COM13", baudrate=9600)

if rec_flag ==1:
    #ser=serial.Serial("COM13", baudrate=9600) # optogenetics
    ser3=serial.Serial("COM5", baudrate=9600)
    
    #ser.write('3')
    #trials = 100

if ppl_flag == 1:
    script = r"C:\Users\Achub_Lab\Desktop\Vis Stim\Save_video_sockets_G-1-G---G (Drifting)_Pupillometry.py"
    theproc = Popen(["python", script])
    core.wait(0.5)
    
if speed_flag == 1:
    ser_speed = serial.Serial("COM9", baudrate=9600) 
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename =  'speed_' + str(date) + '.pkl'
    output = open(filename, 'wb')
    print filename

#create a window
win = visual.Window( [1920,1080], 
                        monitor="mymon", 
                        units="pix", 
                        fullscr=True,
                        screen = 2, 
                        winType = 'pyglet',
                        colorSpace ='rgb',
                        color=0,
                        allowGUI=False
                       )

temporal_freq = 2 # Hz
spatial_freq= 0.04 #c/deg
phase_advance= temporal_freq/60.0 # monitor refresh rate 60 Hz
angle_iteration=30
orientations_number=12
duration = 0.4
frames = int(duration *60)

cycle0=1
cycle1=10
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

grating2 = visual.GratingStim(win, 
                            mask='circle',
                            tex = 'sin', 
                            size=300, 
                            #opacity = 0.5,
                            pos=[0,0], 
                            sf=spatial_freq, 
                            ori = angle_iteration*cycle1, 
                            phase = 0)
                            
noiseTexture = random.rand(16,16)*2.0-1.0
speed = 256
myPatch = visual.GratingStim(win, tex=noiseTexture, 
    size= 2500, units='pix',
    interpolate=False, mask='circle', ori = angle_iteration*cycle0,
    autoLog=False)#this stim changes too much for autologging to be useful
    #add ori=30 to set orientation.  make phase to be 180 without ori, then set ori
    

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
if opto_flag==1:
    ser_opto.write('3')
if rec_flag ==1:
    #ser=serial.Serial("COM13", baudrate=9600) # optogenetics
  
    ser3.write('3')

trial_type = 0
# 0 = G-1 only
# 1 = G-1-G-10
# 2 = G-1-G-N
# 3 = G-N only
for ii in range(trials):

    buff = 'Camera start'
    if ppl_flag == 1:  
        clientsocket.send('Hi there!') #This message triggers opening of video cap & rec start
        print 'Sent', ii+1
        buff = connection.recv(32)
    
    if speed_flag ==1:    
        ser_speed.write('1') 
            
    if buff == 'Camera start':
        if opto_flag==1:
            ser_opto.write('1')
        if rec_flag ==1:
            
            ser3.write('1')
            #ser.write('1')
        core.wait(0.5) #units in seconds
        if trial_type !=3:
            for frameN in range(frames):
                grating.setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
                #grating.phase=0
                grating.draw()
                #grating2.draw()
                win.flip()     
#                win.getMovieFrame()
            grating.setPhase(0)    
            win.flip() 
            
            core.wait(1)#0.25, 0.125, 0.0625
        
        if trial_type == 1: # familiar
            for frameN in range(frames):
                grating2.setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
                #grating.phase=0
                grating2.draw()
                win.flip()
            grating2.setPhase(0)
            win.flip()
        elif trial_type > 1: # novel stim
            for frameN in range(frames):
                myPatch.phase += (1 / speed, 0 / speed)  # increment by (1, 0) pixels per frame
                myPatch.draw()
                win.flip()
            win.flip()
        else:
            core.wait(1) # omission

        x = randint(5,8)
        # print x
        core.wait(x)
        if speed_flag ==1:
            ser_speed.write('2')
            x2 = ser_speed.readline()
            #print x2
            try:
                pickle.dump(x2, output)
            except:
                print ('data not written')
#Win.close()
#win.saveMovieFrames(fileName='30deg_grating.mp4') 
clientsocket.send('Finished')
output.close()

 