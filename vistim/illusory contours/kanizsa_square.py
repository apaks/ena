# change the color of background (to black) for the positive control 
# psychopy code from https://www.programmingvisualillusionsforeveryone.online/scripts.html
# Alex Pak, 2017
# trial length 2s, 6*200=1200s, 20 min
# opto Arduino = 900 ms, duration = 800 ms, 100 ms before transition
`
import math, numpy, random #to have handy system and math functions 
from psychopy import core, event, visual, gui #these are the psychopy libraries
import serial, time
import numpy as np
from subprocess import Popen
import socket #for connecting to other programs
import sys

type = 4 #1 = Kanizsa ic, 2 = rotated pac man, 3 = square, 4 = line, 5 amodal figure

trial_seq = [3, 3, 1, 4, 3, 4, 4, 1, 4, 4, 2, 1, 4, 4, 3, 4, 4, 3, 2, 4, 3, 2, 3, 4, 4, 2, 2, 3, 4, 4, 4, 4, 2, 2, 3, 1, 2, 3, 1, 1, 2, 4, 2, 4, 1, 2, 4, 2, 4, 4, 3, 2, 4, 3, 3, 2, 3, 2, 1, 1, 4, 4, 2, 4, 4, 3, 2, 3, 1, 1, 3, 2, 2, 1, 1, 1, 1, 1, 4, 2, 4, 2, 3, 3, 2, 1, 3, 3, 2, 1, 3, 1, 2, 3, 4, 4, 2, 4, 1, 3, 2, 1, 1, 4, 4, 3, 1, 3, 3, 4, 1, 1, 3, 3, 3, 2, 3, 1, 1, 4, 2, 1, 4, 4, 4, 2, 2, 2, 4, 3, 4, 3, 2, 1, 1, 2, 1, 4, 3, 4, 3, 2, 3, 1, 3, 1, 2, 3, 2, 1, 1, 4, 1, 1, 1, 1, 3, 2, 1, 1, 3, 3, 3, 2, 1, 1, 1, 3, 2, 2, 3, 1, 4, 2, 1, 2, 4, 1, 3, 2, 4, 4, 3, 2, 4, 2, 3, 2, 1, 4, 3, 3, 1, 3, 2, 2, 1, 2, 2, 4]
trial_seq_amodal = [3, 3, 1, 5, 3, 5, 5, 1, 5, 5, 2, 1, 5, 5, 3, 5, 5, 3, 2, 5, 3, 2, 3, 5, 5, 2, 2, 3, 5, 5, 5, 5, 2, 2, 3, 1, 2, 3, 1, 1, 2, 5, 2, 5, 1, 2, 5, 2, 5, 5, 3, 2, 5, 3, 3, 2, 3, 2, 1, 1, 5, 5, 2, 5, 5, 3, 2, 3, 1, 1, 3, 2, 2, 1, 1, 1, 1, 1, 5, 2, 5, 2, 3, 3, 2, 1, 3, 3, 2, 1, 3, 1, 2, 3, 5, 5, 2, 5, 1, 3, 2, 1, 1, 5, 5, 3, 1, 3, 3, 5, 1, 1, 3, 3, 3, 2, 3, 1, 1, 5, 2, 1, 5, 5, 5, 2, 2, 2, 5, 3, 5, 3, 2, 1, 1, 2, 1, 5, 3, 5, 3, 2, 3, 1, 3, 1, 2, 3, 2, 1, 1, 5, 1, 1, 1, 1, 3, 2, 1, 1, 3, 3, 3, 2, 1, 1, 1, 3, 2, 2, 3, 1, 5, 2, 1, 2, 5, 1, 3, 2, 5, 5, 3, 2, 5, 2, 3, 2, 1, 5, 3, 3, 1, 3, 2, 2, 1, 2, 2, 5]
opto_idx = [1, 2, 3, 5, 9, 10, 12, 15, 21, 24, 25, 28, 29, 31, 32, 34, 35, 36, 41, 43, 44, 45, 47, 48, 49, 50, 51, 52, 54, 57, 62, 64, 67, 68, 71, 76, 79, 80, 81, 84, 86, 87, 88, 91, 92, 96, 98, 99, 102, 104, 106, 107, 108, 109, 110, 111, 112, 113, 114, 120, 121, 122, 128, 129, 131, 133, 138, 139, 140, 142, 143, 144, 147, 148, 149, 150, 151, 153, 155, 158, 159, 161, 162, 163, 165, 170, 172, 173, 177, 181, 183, 186, 188, 189, 190, 192, 194, 196, 197, 198]
short_seq = np.array(trial_seq)[opto_idx]

x,y =  -150, -100  # set posiiton based on population RF responses 
#x, y = 250, -100 part of kic 
#x, y = 250, 100 not part of kic bot left 
myWin = visual.Window(color='grey', 
        units='pix', size=[1920,1080], 
        screen = 1,
        allowGUI=False, 
        fullscr=True) #creates a window

#myClock = core.Clock() #this creates and starts a clock which we can later read
rec_flag = 0
opto_flag = 0
ppl_flag = 0

trials = 20
r = 125

if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)
    trials = 20

if opto_flag==1:
    ser_opto=serial.Serial("COM13", baudrate=9600)

if ppl_flag == 1:
    script = r"C:\Users\Achub_Lab\Desktop\Vis Stim\Save_video_sockets_G-1-G---G (Drifting)_Pupillometry.py"
    theproc = Popen(["python", script])
    core.wait(0.5)
    

disc = visual.Circle(myWin, 
    radius=r, 
    fillColor='black', 
    vertices = 128,
    lineColor = None)

disc_outline = visual.Circle(myWin, 
    radius = r, 
    fillColor= None,
    vertices = 128,
    lineColor = 'black', lineWidth = 30)

def draw_4discs(a, x, y):
    disc.setPos([-a+x,-a+y]) 
    disc.draw()
    disc.setPos([a+x,-a+y])
    disc.draw()
    disc.setPos([-a+x,a+y])
    disc.draw()
    disc.setPos([a+x,a+y])
    disc.draw()
    
def draw_4discs_lines(a, x, y):
    disc_outline.setPos([-a+x,-a+y]) 
    disc_outline.draw()
    disc_outline.setPos([a+x,-a+y])
    disc_outline.draw()
    disc_outline.setPos([-a+x,a+y])
    disc_outline.draw()
    disc_outline.setPos([a+x,a+y])
    disc_outline.draw()

square = visual.Rect(myWin, width = 600, 
            height=600, fillColor='grey', 
            lineColor=None)
                       
square_small = visual.Rect(myWin, width=150, 
            height=150, fillColor='grey', 
            lineColor=None)


    
framerate=60 # Hz
duration = 0.5 # in sec
frames = int(duration*framerate)

if rec_flag==1:

    ser.write('3')
if opto_flag==1:
    ser_opto.write('3')

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

core.wait(4)
for i, val in enumerate(short_seq):
#    val = 1
    square.opacity = 1
    if val == 4:
        square.lineColor = 'black'
        square.fillColor = 'grey'
        square.lineWidth = 10
    else:
        square.lineColor = 'grey'
        square.fillColor = 'grey'
    if val == 3:
        square.fillColor = 'white' 
        # square.opacity = 0.1
    else:
        square.fillColor = 'grey' 
    
        
#    t1 = time.time()
    if i%20==0:
        print i
    if ppl_flag == 1:  
        clientsocket.send('Hi there!') #This message triggers opening of video cap & rec start
        buff = connection.recv(32)
    if rec_flag==1:
        ser.write('1')
    if opto_flag == 1:
        if i in opto_idx:
            ser_opto.write('1')

        
    core.wait(0.5)    
     
    for i in range(frames):
        draw_4discs(300,x, y)
        myWin.flip()

    if val == 1 or val ==5:
        
        for i in range(frames):
            draw_4discs(300,x, y)
            square.setPos([x, y])
            square.draw()
            if val == 5:
                draw_4discs_lines(300,x, y)
            myWin.flip()
#        myWin.getMovieFrame()
#        myWin.saveMovieFrames(fileName='kanizsa_{val}.bmp'.format(val=str(val) )) 
    
        myWin.flip()
#        t2 = time.time() 
    elif val == 2:
        
        for i in range(frames):
            draw_4discs(300,x, y)
            square_small.setPos([-300+x + (r/2), -300+y+(r/2)])
            square_small.draw()
            square_small.setPos([300+(r/2)+x, 300+(r/2)+y])
            square_small.draw()
            square_small.setPos([-300 - (r/2)+x, 300 + (r/2)+y])
            square_small.draw()
            square_small.setPos([300 + (r/2)+x, -300 - (r/2)+y])
            square_small.draw()
            myWin.flip()

        myWin.flip()
#        t2 = time.time() 
    else:
        
        for i in range(frames):
            square.setPos([x, y])
            square.draw()
            myWin.flip()

        myWin.flip()
#        t2 = time.time() 
#    print t2 -t1
    core.wait(3)  #waits for 5 seconds

myWin.close() #closes the window
core.quit() #quits


