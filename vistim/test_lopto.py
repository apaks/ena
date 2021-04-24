
import serial
from psychopy import visual, core

ephys_flag = 0
opto_flag = 1

if ephys_flag==1:
    ser2=serial.Serial("COM5", baudrate=9600)
    ser2.write('3')
    
if opto_flag==1:    
    ser=serial.Serial("COM13", baudrate=9600)
    ser.write('3')


mywin = visual.Window( [1920,1080], 
                        monitor="mymon", 
                        units="deg", 
                        screen = 2,
                        winType = 'pyglet',
                        colorSpace ='rgb',
                        color=0)


tf = 2
spatial_freq=0.05 #0.05 #Grating width (higher => more, thinner bars)      0.05 G-3-G-4
phase_advance= tf/60.0 #0.05; Drift speed, this is the approx range for strong murine OKR 0.1 G 3
angle_iteration=30 #30
orientations_number=12 #11, 12
orientation_latency=12 #12 #units are in frames? 1/60 = duration of 1 frame.  (1/60)12 = 0.2s = 200ms.


cycle0= 1 #1  5 G 3





grating = visual.GratingStim(win=mywin, 
                            mask='circle',
                            tex = 'sin', 
                            size=300, 
                            pos=[0,0], 
                            sf=spatial_freq, 
                            ori = angle_iteration*cycle0, 
                            phase = 0)


mywin.flip()
core.wait(4)

for i in range(20):
    if ephys_flag == 1:
        ser2.write('1')

    core.wait(1)
    if opto_flag ==1:
        ser.write('1')
    for frameN in range(orientation_latency):
        grating.setPhase(phase_advance, '+')#advance phase by 0.05 of a cycle
        #grating[cycle0].phase=0
        #grating.draw()
        mywin.flip()  
    mywin.flip()  
    core.wait(1)
    print i
    
    core.wait(12)