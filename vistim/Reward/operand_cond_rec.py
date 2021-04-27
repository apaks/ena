# Alex Chubykin, 2012, Sam Kissinger 2015, Alex Pak 2016


from psychopy import visual, core #import some libraries from PsychoPy
#import socket #for connecting to other programs
import sys
import datetime
import time
from random import randint
import pickle
import serial
connected=False
ser=serial.Serial("COM6", baudrate=9600)
ser1=serial.Serial("COM11", baudrate=9600)
ser3=serial.Serial("COM5", baudrate=9600)
#Create a window
mywin = visual.Window( [1920,1080], 
                        monitor="mymon", 
                        units="deg", 
                        screen=1, 
                        winType = 'pyglet',
                        colorSpace ='rgb',
                        color=0)

#Create some stimuli

tf = 1     # Hz
spatial_freq=0.04     #Grating width (higher => more, thinner bars)
phase_advance=tf/60.0 #0.005; Drift speed, this is the approx range for strong murine OKR
angle_iteration=30 #180
orientations_number=12 #11, 12
orientation_latency=60 #units are in frames? 1/60 = duration of 1 frame.  (1/60)12 = 0.2s = 200ms.


cycle0=1
cycle1=2

grating = visual.GratingStim(win=mywin, 
                            mask='circle',
                            tex = 'sin', 
                            size=300, 
                            pos=[0,0], 
                            sf=spatial_freq, 
                            ori = angle_iteration*cycle0, 
                            phase = 0)

#Draw the stimuli and update the window - example

now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d_%H-%M-%S")



filename =  'lick_times_' + str(date) + '.pkl'
print filename
output = open(filename, 'wb')

mywin.flip()
end_tick = 0

core.wait(4.0)
ser.write('3')

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
random_seq = [1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1]
#random_seq = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  
#random_seq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


for ii in range(len(random_seq)): #number of recordings
#    clientsocket.send('Hi there!') #This message triggers opening of video cap & rec start
#    print 'Sent', ii+1
    #DataValue=ser.read()
    ser1.write('3')
    
    x =ser1.readline()
    
    print x
    
    
    try:
        
        pickle.dump(x, output)
        
    except:
        print ('data not written')
#    buff = connection.recv(32)
        
#    if buff == 'Camera start':
    #if buff == 'server ready': #This should be sent right after the video capture is opened
    
    

    DataValue = 1
#        print 'Cycle starts at:', datetime.datetime.now().time()
    if DataValue != None:
        print 'TTL signal received',ii
        ser3.write('1')
        core.wait(0.5) #units in seconds
            
        for frameN in range(orientation_latency):
            grating.setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
            #grating[cycle0].phase=0
            grating.draw()
            mywin.flip()    
        mywin.flip()   
        #core.wait(1.0)

        tick = 6

        if random_seq[ii]==0:
            tick = -5
        
        for frameN in range(120):
      
            ser1.write('5')
            
            flag = ser1.readline()
            
           
            if flag[0]=='t':
               tick = tick + 1
            if tick>2:
                end_tick = 0
                ser.write('1')
                core.wait(1)
                break
                
        print tick

        mywin.flip()
        

 
     
        r = randint(10,15)
        #print r
        core.wait(r)#this wait = 7.7 instead of 7.  Accounts for the 0.5s after stim #1, and 200ms of stim2
#        print 'Cycle ends at: ', datetime.datetime.now().time(), '\n'
    grating.setPhase(0)
output.close()
#clientsocket.send('Finished')