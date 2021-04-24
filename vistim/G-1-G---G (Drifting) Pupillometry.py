# Alex Chubykin, 2012, Sam Kissinger 2015
from __future__ import division
from psychopy import visual, core #import some libraries from PsychoPy
import socket #for connecting to other programs
import sys
import datetime
import time
import serial, pickle

speed_flag = 1

from subprocess import Popen#NEW

script = r"c:\Sam Visual Stim\G-1-G---G_or_G-1-G-2-G Save_video_sockets.py"#NEW
#script = r"c:\Sam Visual Stim\Optokinetic_save_video_sockets.py"
#Run the script
theproc = Popen(["python", script])#NEW

#######Speed#######
if speed_flag == 1:
    ser_speed = serial.Serial("COM8", baudrate=9600) 
    #ser_speed = serial.Serial("COM8", baudrate=115200) # 12/14/2018 important change. make sure the speed of arduino serial is the same as here
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename =  'speed_' + str(date) + '.pkl'
    print filename
    output = open(filename, 'wb')
    ser_speed.write('3')
#######Speed#######

connected=False
ser=serial.Serial("COM5", baudrate=9600)
#ser1=serial.Serial("COM7", baudrate=9600)############FOR LASER#############

#Create a window
mywin = visual.Window([1920,1080],monitor="Sam", units="deg", screen=2,fullscr='True')

#Create some stimuli
grating=[]
spatial_freq=0.03 #Samdefault = 0.1 on old default settings 0.035 on corrected settings.#Grating width (higher => more, thinner bars)#0.3
phase_advance=0.05#Samdefault = 0.05 Drift speed PA = temporal freq/frame rate.  So x/60fps = 0.05 x=3Hz
angle_iteration=30 #180
orientations_number=12 #11, 12
orientation_latency=12 #12 #units are in frames? 1/60 = duration of 1 frame.  (1/60)12 = 0.2s = 200ms,  24 = 0.4, 48 = 0.8, 96 = 1.6s

#Under this spatial_freq & phase_advance,
#the pupil moves slowly along with the direction of drifting and it moves back suddenly == OKR

cycle0=2#2
cycle1=4#4


for i in range(orientations_number):
    grating.append(visual.PatchStim(win=mywin, mask="circle", size=500, pos=[0,0], sf=spatial_freq, ori=i*angle_iteration, phase = 0))
fixation = visual.PatchStim(win=mywin, size=500, pos=[0,0], sf=0, color='gray')


core.wait(4.0)
ser.write('3')
#ser1.write('3')############FOR LASER#############

#Sockets client
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8090))#8089
#
print 'Stimuli listen ready\n';
sys.stdout.flush();
#
#Sockets server
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8091)) #8089
serversocket.listen(5) # become a server socket, maximum 5 connections
connection, address = serversocket.accept()

#Stim/window prep
fixation.draw() #Draw gray screen now to eliminate future processing time?
mywin.update()

#Cycling of stimulus
#while 1: #Infinite stimulus repeat
for ii in range(40): #number of recordings
    clientsocket.send('Hi there!') #This message triggers opening of video cap & rec start
    print 'Sent', ii+1
    DataValue=ser.read()
    buff = connection.recv(32)
    #######Speed#######
    if speed_flag ==1:    
        ser_speed.write('1')
    #######Speed#######
        
    if buff == 'Camera start':
    #if buff == 'server ready': #This should be sent right after the video capture is opened
        
        print 'Cycle starts at:', datetime.datetime.now().time()
    
    if DataValue != None:
        print 'TTL signal received'
        print ii
    ser.write('1')
    #ser1.write('1')############FOR LASER#############
    core.wait(2.0) #units in seconds
            
    for frameN in range(orientation_latency):
        grating[cycle0].setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
        #grating[cycle0].phase=0.5#This line instead of above for static stim. Set phase to 0.5 to keep black bar in center of screen
        grating[cycle0].draw()
        #mywin.update()
        mywin.flip()

    #core.wait(0.2)

#    fixation.draw()
#    mywin.update()
#    core.wait(1.0)#0.5, 0.25, 0.125, 0.0625, 0.03125
#        
#    for frameN in range(orientation_latency):
#        grating[cycle1].setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
#        #grating[cycle1].phase=0#This line instead of above for static stim.
#        grating[cycle1].draw()
#        #mywin.update()
#        mywin.flip()    
                
    #fixation.draw()
    mywin.flip()
    #core.wait(1.0)
    core.wait(6.0)#keeps 8.4s between the time serial 1 is written. 7.7 for G-1, 6.5 for G1G2
    grating[cycle0].setPhase(0)#to make sure phase starts at same place each presentation
    print 'Cycle ends at: ', datetime.datetime.now().time(), '\n'

#######Speed#######
    if speed_flag ==1:
        ser_speed.write('2')
        x2 = ser_speed.readline()
        print x2
        try:
            pickle.dump(x2, output)
        except:
            print ('data not written')
#######Speed#######
    core.wait(0.5)#THis was added as a safety (after 2018.10.03 FX data set) 
mywin.close()
clientsocket.send('Finished')
#######Speed#######
output.close()
#######Speed#######