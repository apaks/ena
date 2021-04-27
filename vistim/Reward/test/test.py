# Alex Chubykin, 2012, Sam Kissinger 2015

from psychopy import visual, core #import some libraries from PsychoPy
#import socket #for connecting to other programs
import sys
import datetime
import time
import sys


import serial
connected=False
ser=serial.Serial("COM3", baudrate=9600)


#sys.stdout = open('file', 'w')



#Create a window 
mywin = visual.Window([1920,1080],monitor="testMonitor", units="deg", screen=1)

#Create some stimuli
grating=[]
spatial_freq=0.04 #Grating width (higher => more, thinner bars)
phase_advance=0.05 #0.005; Drift speed, this is the approx range for strong murine OKR
angle_iteration=30 #180
orientations_number=12 #11, 12
orientation_latency=12 #units are in frames? 1/60 = duration of 1 frame.  (1/60)12 = 0.2s = 200ms.

#Under this spatial_freq & phase_advance,
#the pupil moves slowly along with the direction of drifting and it moves back suddenly == OKR

cycle0=2
cycle1=4


for i in range(orientations_number):
    grating.append(visual.PatchStim(win=mywin, mask="circle", size=70, pos=[0,0], sf=spatial_freq, ori=i*angle_iteration))
fixation = visual.PatchStim(win=mywin, size=70, pos=[0,0], sf=0, color='gray')

#Draw the stimuli and update the window - example

#grating.draw()
fixation.draw()
mywin.update()


core.wait(4.0)

'''
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
'''
#Cycling of stimulus
#while 1: #Infinite stimulus repeat
for ii in range(200): #number of recordings
#    clientsocket.send('Hi there!') #This message triggers opening of video cap & rec start
#    print 'Sent', ii+1
    ser.write('3')
    DataValue=ser.readline()
    
    print DataValue
    
#    buff = connection.recv(32)
        
#    if buff == 'Camera start':
    #if buff == 'server ready': #This should be sent right after the video capture is opened
        
#        print 'Cycle starts at:', datetime.datetime.now().time()
    if DataValue != None:
        print 'TTL signal received',ii
        ser.write('1')
        core.wait(0.5) #units in seconds
            
        for frameN in range(orientation_latency):
            grating[cycle0].setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
            #grating[cycle0].phase=0
            grating[cycle0].draw()
            mywin.update()    

        fixation.draw()
        mywin.update()
        core.wait(1.0)
        
        for frameN in range(orientation_latency):
         #   grating[cycle].setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
            #grating[cycle1].phase=0
          #  grating[cycle1].draw()
            mywin.update()
                
        fixation.draw()
        mywin.update()
        core.wait(7.2)#this wait = 7.7 instead of 7.  Accounts for the 0.5s after stim #1, and 200ms of stim2
#        print 'Cycle ends at: ', datetime.datetime.now().time(), '\n'

#clientsocket.send('Finished')