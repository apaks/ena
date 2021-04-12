# study motion coherence by RDK tuning. duration Arduino 2 sec
# Alex Pak, 2017

from __future__ import division
from psychopy import visual, core
import serial
from random import randint

rec_flag = 0

if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)
    trials = 20

coherence = [0.5, 0.7, 1, 0.2, 0.2, 0, 0, 0.5, 1, 0.7, 0.2, 0.5, 1, 0, 0.5, 0, 0.5, 0.7, 0.2, 1, 
0.7, 0.2, 0.2, 0.7, 1, 0.7, 0.7, 0, 0.2, 0.5, 0.7, 0, 0, 1, 0.7, 0.7, 0.2, 0.7, 
0.7, 1, 0.5, 1, 0, 1, 0.5, 0.2, 1, 0, 0.7, 0.7, 0.5, 0, 0.2, 0.5, 1, 0.5, 0, 0.7, 
1, 0, 1, 0.7, 0, 0.2, 0.5, 1, 0.5, 0.7, 0, 0.7, 0, 1, 0.7, 0.2, 1, 0.5, 0.2, 1, 
0.2, 0.7, 0.2, 0.5, 0.2, 0, 0.2, 1, 1, 1, 0.5, 0, 0, 0, 0.2, 0.5, 0.2, 0.5, 0, 
0.5, 0.5, 0.2]

trials = 100
myWin = visual.Window( [1920,1080], 
                        monitor="testMonitor", 
                        units=  'pix',
                        screen=2, 
                        fullscr= 'True',
                        #winType = 'pyglet',
                        colorSpace ='rgb',
                        color = -1,
                       )
                       
dot_stim =visual.DotStim(myWin, 
    dir=270, nDots=50, fieldShape='circle', fieldSize = 1920 , dotSize = 2400,
    dotLife = 20, coherence = 1, speed = 0.01)

dot_stim.setFieldCoherence(0.7)
#dotPatch.set('coherence',0.0)
duration = 1
frames = int(60*duration)
#timer = core.Clock()
#timer.reset()

core.wait(4)
if rec_flag==1:

    ser.write('3')
    #ser2.write('3')
    
for j in range(trials):
   
    dot_stim.setFieldCoherence(coherence[j])
    print 'trial',j
    if rec_flag==1:
        ser.write('1')
        #ser2.write('1')
    core.wait(0.5)

    for frame in range(frames): 
    #timer.getTime()<10:
        dot_stim.draw()
        myWin.flip()
    myWin.flip() 
    rint = randint(5,10)
    core.wait(rint)
    
    