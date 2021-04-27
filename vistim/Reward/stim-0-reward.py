# Alex Pak, 2016

from psychopy import visual, core #import some libraries from PsychoPy
import socket #for connecting to other programs
import sys
import datetime
import time
import numpy as np
from subprocess import Popen
import serial
from random import randint
#
#connected=False
ser=serial.Serial("COM5", baudrate=9600)# ser COM5 for OpenEphys/Optogenetics Arduino
ser1=serial.Serial("COM6", baudrate=9600)# ser1 COM4 for Lickport Arduino
ser2=serial.Serial("COM11", baudrate=9600)# lick counter


script = r"C:\Users\Achub_Lab\Desktop\Vis Stim\Save_video_sockets_G-1-G---G (Drifting)_Pupillometry.py"
# run script
theproc = Popen(["python", script])

#ser1=serial.Serial("COM6", baudrate=9600)# ser1 COM7 for Laser Arduino
#Create a window
win = visual.Window( [1920,1080], 
                        monitor="testMonitor", 
                        units="deg", 
                        screen=1, 
                        winType = 'pyglet',
                        colorSpace ='rgb',
                        color=0
                       )
#Create some stimuli
temporal_freq = 1.5 # Hz
spatial_freq=0.1 #Grating width (higher => more, thinner bars)
phase_advance= temporal_freq/60.0 #0.005; Drift speed, this is the approx range for strong murine OKR
angle_iteration=30 #180
orientations_number=12 #11, 12
orientation_latency=24 #units are in frames? 1/60 = duration of 1 frame.  (1/60)12 = 0.2s = 200ms.


cycle0=0
cycle1=4


grating = visual.GratingStim(win, 
                            mask='circle',
                            tex = 'sin', 
                            size=300, 
                            pos=[0,0], 
                            sf=spatial_freq, 
                            ori = angle_iteration*cycle0, 
                            phase = 0)




#Sockets client
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8090))#8089
#
print 'Stimuli listen ready\n';
sys.stdout.flush();

#Sockets server
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8091)) #8089
serversocket.listen(5) # become a server socket, maximum 5 connections
connection, address = serversocket.accept()

#Stim/window prep

win.flip()

core.wait(4.0)
ser.write('3')
#ser1.write('3')


#random_seq = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]

random_seq = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]       

#random_seq = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]       

#random_seq = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1]

#random_seq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#random_seq = [1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1]

#Cycling of stimulus

for ii in range(len(random_seq)): #number of recordings
    clientsocket.send('Hi there!') #This message triggers opening of video cap & rec start
    print 'Sent', ii+1
    
    ser2.write('3')
    x=ser2.readline()
    
    print x
    
    DataValue=ser.read()
    buff = connection.recv(32)
    #buff = 'Camera start'
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
            #grating.phase=0
            grating.draw()
            win.flip()    

 
                
      
        win.update()
        grating.setPhase(0) # reset the phase
        r = (randint(15,20)) 
        print r
        core.wait(r)#keeps 8.4s between the time serial 1 is written
        #print 'Cycle ends at: ', datetime.datetime.now().time(), '\n'

clientsocket.send('Finished')