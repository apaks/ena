# Alex Chubykin, 2012, Sam Kissinger 2015

from psychopy import visual, core #import some libraries from PsychoPy
import socket #for connecting to other programs
import sys
import datetime
import time
import numpy as np
import serial
from random import randint

connected=False
ser=serial.Serial("COM5", baudrate=9600)# ser COM5 for OpenEphys/Optogenetics Arduino
ser1=serial.Serial("COM6", baudrate=9600)# ser1 COM4 for Lickport Arduino
ser2=serial.Serial("COM10", baudrate=9600)# lick counter


#ser1=serial.Serial("COM6", baudrate=9600)# ser1 COM7 for Laser Arduino
#Create a window
mywin = visual.Window([1920,1080],monitor="testMonitor", units="deg", screen=1)

#Create some stimuli
grating=[]
spatial_freq=0.3 #Grating width (higher => more, thinner bars)
phase_advance=0.05 #0.005; Drift speed, this is the approx range for strong murine OKR
angle_iteration=30 #180
orientations_number=12 #11, 12
orientation_latency=24 #units are in frames? 1/60 = duration of 1 frame.  (1/60)12 = 0.2s = 200ms.

#Under this spatial_freq & phase_advance,
#the pupil moves slowly along with the direction of drifting and it moves back suddenly == OKR

cycle0=9 #A-6, B=2
cycle1=4

grating = visual.GratingStim(win=mywin, mask='circle',tex = 'sin', size=70, pos=[0,0], 
                                    sf=spatial_freq, ori = angle_iteration*cycle0, phase = 0.25)
#for i in range(orientations_number):
#    grating.append(visual.PatchStim(win=mywin, mask="circle", size=70, pos=[0,0], sf=spatial_freq, ori=i*angle_iteration))
fixation = visual.GratingStim(win=mywin, size=70, pos=[0,0], sf=0, colorSpace ='rgb255',color=[146,146,146])

#Draw the stimuli and update the window - example
"""
grating.draw()
fixation.draw()
mywin.update()

"""
#core.wait(4.0)
#ser.write('3')

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

#Stim/window prep
fixation.draw() #Draw gray screen now to eliminate future processing time?
mywin.update()

core.wait(4.0)
ser.write('3')
#ser1.write('3')


#random_seq = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]

#random_seq = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]       

#random_seq = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]       

random_seq = [1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1]



#Cycling of stimulus
#while 1: #Infinite stimulus repeat
for ii in range(40): #number of recordings
    clientsocket.send('Hi there!') #This message triggers opening of video cap & rec start
    print 'Sent', ii+1
    
    ser2.write('3')
    x=ser2.readline()
    
    print x
    
    DataValue=ser.read()
    buff = connection.recv(32)
        
    if buff == 'Camera start':
    #if buff == 'server ready': #This should be sent right after the video capture is opened
        
        #print 'Cycle starts at:', datetime.datetime.now().time()
        if DataValue != None:
            print 'TTL signal received'
            
    
            if random_seq[ii] == 1:
                ser.write('1')
                ser1.write('1')
            else:
                ser.write('1')
                ser1.write('0')
        core.wait(0.5) #units in seconds
            
        for frameN in range(orientation_latency):
            grating.setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
            #grating[cycle0].phase=0
            grating.draw()
            mywin.flip()    

  
                
        fixation.draw()
        mywin.update()
        
        r = (randint(5,7)) 
        print r
        core.wait(r)#keeps 8.4s between the time serial 1 is written
        #print 'Cycle ends at: ', datetime.datetime.now().time(), '\n'
    grating = visual.GratingStim(win=mywin, mask='circle',tex = 'sin', size=70, pos=[0,0], 
                                    sf=spatial_freq, ori = angle_iteration*cycle0, phase = 0.25)

clientsocket.send('Finished')