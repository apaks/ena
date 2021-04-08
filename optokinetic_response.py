
# Alex Pak, 2019, 2021
# optokinetic stimulus: tf = 1.5 Hz, sf = 0.125 cyc/deg 
# ephys 25 s, 5s base, 20s stim, 5s after stim
# 10 trials, 3 tf
from psychopy import visual, core #import some libraries from PsychoPy
import datetime, sys
import socket #for connecting to other programs
import serial, pickle
from random import randint
from scipy import random 
import numpy as np
from subprocess import Popen
connected=False

ppl_flag = 1
ephys_flag = 0
speed_flag = 0

if ephys_flag == 1:
    #ser=serial.Serial("COM13", baudrate=9600) # optogenetics
    ser_ephys = serial.Serial("COM5", baudrate=9600)
    
if speed_flag == 1:
    ser_speed = serial.Serial("COM8", baudrate=9600) 
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename =  'speed_' + str(date) + '.pkl'
    print (filename)
    output = open(filename, 'wb')
    ser_speed.write('3')

if ppl_flag == 1:
    script = r"C:\Users\AChub_Lab\Desktop\psychopy-okr\pupil_sockets_instrum.py"
    theproc = Popen(["python", script])
    core.wait(0.5)
    
tf_seq = np.array([2. , 1.5, 3. , 2. , 1.5, 3. , 3. , 2. , 1.5, 3. , 2. , 1.5, 2. ,
       3. , 1.5, 3. , 3. , 2. , 1.5, 1.5, 2. , 2. , 2. , 1.5, 2. , 3. ,
       3. , 1.5, 3. , 1.5])


#create a window
win = visual.Window( [600,600], 
                        monitor="mymon", 
                        units="deg", 
                        fullscr=False,
                        screen = 1, 
                        # winType = 'pyglet',
                        colorSpace ='rgb',
                        color=0,
                        allowGUI=True
                       )


temporal_freq = 2 # Hz
spatial_freq= 0.04 #c/deg
phase_advance= temporal_freq/60.0 # monitor refresh rate 60 Hz
duration = 1
frames = int(duration *60)

cycle0=0

#create some stimuli
grating = visual.GratingStim(win, 
                            mask='circle',
                            tex = 'sin', 
                            size= 50, 
                            pos=[0,0], 
                            #opacity = 1,
                            sf=spatial_freq, 
                            ori = 0, 
                            phase = 0)


if ppl_flag == 1:

    #Sockets client
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8090))#8089

    print ('Stimuli listen ready')
    sys.stdout.flush()

    #Sockets server
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 8091)) #8089
    serversocket.listen(5) # become a server socket, maximum 5 connections
    connection, address = serversocket.accept()


win.flip()
core.wait(4.0)
if ephys_flag == 1:
    #ser=serial.Serial("COM13", baudrate=9600) # optogenetics
    ser_ephys.write('3')

for idx, val in enumerate(tf_seq[:5]):
    print (idx, val)
    phase_advance= tf_seq[idx]/60.0
#    val = 2
    
    if ppl_flag == 1:  
        clientsocket.send(b'Hi there!') #This message triggers opening of video cap & rec start
        buff = connection.recv(32)
        print ('Trial started at time:', datetime.datetime.now().time())
    else:
        buff = 'go'
 
    
    if len(buff) > 0:
        if speed_flag ==1:
            ser_speed.write('1') 
        if ephys_flag == 1:
            ser_ephys.write('1')

        core.wait(0.5) #units in seconds

        for frameN in range(frames):
            grating.setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
            grating.draw()
            win.flip()     
        win.flip() 


        core.wait(1)
        if speed_flag ==1:
            ser_speed.write('2')
            x2 = ser_speed.readline()
#            print x2
            try:
                pickle.dump(x2, output)
            except:
                print ('data not written')
        core.wait(5)

clientsocket.send(b'Finished')
core.wait(3)
win.close()
output.close()




 