import numpy as np
from psychopy import core, event, visual
from random import randint
import serial

win = visual.Window(
        size=[1920,1080], 
        units='pix', 
        screen = 1,
#        allowGUI=False, 
        color=1, 
        fullscr = True
        ) #creates a window

rec_flag = 0

if rec_flag ==1:
    #ser=serial.Serial("COM13", baudrate=9600) # optogenetics
    ser = serial.Serial("COM5", baudrate=9600)

dir12_seq = [10, 7, 3, 2, 4, 8, 9, 5, 7, 3, 4, 8, 3, 2, 1, 8, 0, 4, 9, 11, 
10, 9, 1, 11, 4, 0, 7, 1, 2, 8, 2, 9, 11, 9, 6, 5, 10, 4, 9, 0, 7, 11, 9, 
5, 9, 10, 11, 6, 8, 9, 5, 4, 2, 8, 11, 2, 10, 3, 5, 1, 7, 0, 4, 9, 1, 5, 
11, 3, 5, 10, 1, 2, 9, 6, 2, 2, 11, 5, 10, 7, 3, 7, 4, 6, 8, 4, 1, 8, 0, 
11, 0, 6, 2, 11, 1, 10, 3, 8, 3, 1, 2, 10, 5, 3, 11, 1, 7, 3, 4, 7, 8, 4, 6, 
7, 11, 7, 0, 8, 6, 10, 4, 5, 7, 2, 10, 3, 5, 9, 8, 6, 3, 2, 0, 11, 0, 6, 10, 
0, 7, 4, 5, 0, 10, 6, 8, 10, 3, 11, 9, 0, 5, 1, 3, 7, 0, 6, 9, 1, 6, 10, 5, 
6, 11, 7, 0, 5, 1, 4, 1, 6, 8, 2, 9, 2, 8, 3, 0, 4, 6, 1]


cell_size = 2048
line_width = 128

cell = np.ones((cell_size, cell_size))

cell[
    (cell_size // 4) - (line_width // 2):(cell_size // 4) + (line_width // 2),
    :(cell_size // 2)
] = -1

cell[
    (cell_size // 4 * 3) - (line_width // 2):(cell_size // 4 * 3) + (line_width // 2),
    (cell_size // 2):
] = -1

n_vert = 15
n_horiz = 20

phase = 0.0
ori = 0.0
angle_iteration = 30

duration = 5
frames = int(duration * 60)
temporal_freq =1 # Hz
phase_advance= temporal_freq/60.0 # monitor refresh rate 60 Hz

stim = visual.GratingStim(
    win=win, 
    tex=cell, 
    mask="None",
    ori = dir12_seq[0]*angle_iteration,
    size=(cell_size, cell_size)
)

stim.sf = (n_horiz / cell_size, n_vert / cell_size)
stim.size = (cell_size, cell_size )
# sf[0] -> illusory contotur sf, sf[1] gap between inducing lines
# 1 illusory contour, low
stim.sf = (0.0005, 0.0025)

# 3 illusory contours contours, med
stim.sf = (0.001, 0.005)

# 6 illusory contours contours, high
#stim.sf = (0.002, 0.01) 

core.wait(4)
for idx, val in enumerate(dir12_seq): #number of trials
    #print idx, val*30
    stim.setOri(210)
    if rec_flag == 1:
        ser.write('1')
    core.wait(0.3) #units in seconds
                
    for frameN in range(frames):
        stim.phase = [stim.phase[0] + phase_advance, 0]
        stim.draw()
        win.flip()
        
        win.getMovieFrame()
    win.flip() 
#    win.getMovieFrame()
#    win.saveMovieFrames(fileName='abut_grating.mp4')
    
#    stim.setOri(angle_iteration*dir12_seq[idx+1])
#    stim.setPhase(0)
    
    x = randint(3,4)

    core.wait(x)

 