
# Alex Pak, 2016

from psychopy import visual, core #import some libraries from PsychoPy
import time
import serial
from random import randint

#ser=serial.Serial("COM13", baudrate=9600)
#ser3=serial.Serial("COM5", baudrate=9600)
#create a window

win = visual.Window( [1920,1080], 
                        monitor="mymon", 
                        units="deg", 
                        screen=1, 
                        winType = 'pyglet',
                        colorSpace ='rgb',
                        color=0
                       )




temporal_freq = 0 # Hz
spatial_freq= 0.05
phase_advance= temporal_freq/60.0 # monitor refresh rate 60 Hz
angle_iteration=30
orientations_number=12
orientation_latency= 2400 # units are in frames? 1/60 = duration of 1 frame.  (1/60)12 = 0.2s = 200ms.

cycle0=1
cycle1=4
#create some stimuli
grating = visual.GratingStim(win, 
                            mask='gauss',
                            tex = 'sin', 
                            size=100, 
                            pos=[0,0], 
                            opacity = 1,
                            sf=spatial_freq, 
                            ori = angle_iteration*cycle0, 
                            phase = 0)

grating2 = visual.GratingStim(win, 
                            mask='circle',
                            tex = 'sin', 
                            size=300, 
                            opacity = 0.5,
                            pos=[0,0], 
                            sf=spatial_freq, 
                            ori = angle_iteration*cycle1, 
                            phase = 0)

dotPatch = visual.DotStim(win, color=(0, 1.0, 0), 
    nDots=50000, fieldShape='circle', fieldPos=(0.0, 0.0), fieldSize=3,
    dotLife=1,  # number of frames for each dot to be drawn
    signalDots='same',  # are signal dots 'same' on each frame? (see Scase et al)
    #noiseDots='direction',  # do the noise dots follow random- 'walk', 'direction', or 'position'
    #speed=0.01, 
    #coherence=0.9
    )
#
#ser3.write('3')
#ser.write('3')
win.flip()
core.wait(4.0)



for ii in range(20):
#    for frameN in range(10):
#        dotPatch.draw()
#        win.flip()
    print 'TTL signal received',ii
#    
#    win.flip()
#    ser3.write('1')
#    ser.write('1')
    core.wait(0.5) #units in seconds
    #units in seconds?
    for frameN in range(orientation_latency):
        grating.setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
        #grating.phase=0
        grating.draw()
        #grating2.draw()
        win.flip()     
        
    win.flip() 
    #core.wait(2)#0.25, 0.125, 0.0625

#    for frameN in range(orientation_latency):
#        grating2.setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
#        #grating.phase=0
#        grating2.draw()
#        win.flip()
        

    win.flip()

    grating.setPhase(0)
    grating2.setPhase(0)

    x = randint(5,10)
    # print x
    core.wait(x)



    core.wait(3) 
