# study motion coherence by RDK
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


trials = 20
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
    
    