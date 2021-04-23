# Alex Pak, 2018
# MMN paradigm by using bp filtered noise + tf (sin into depth) 
# to make sure that RF responses not biased to articular stim

from __future__ import division
from psychopy import visual, core, event
from psychopy.visual import filters
import numpy as np
import scipy.misc
import wx, os
import serial


rec_flag = 0
if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)
    
ls_file = []

path = r"U:\Visual Stimulation\pak6\Vis Stim\vmmn_paradigms\vmmn_movies"
for file in os.listdir(path):
    if file.endswith(".mp4"):
        ls_file.append(os.path.join(path, file))
ls_file = sorted( ls_file, key=lambda a: int(a.split('\\')[-1].split('_')[-1].split('.')[0] ))

    
win = visual.Window(
    monitor = 'mymon',
    size= [1920,1080],
    screen=2,
    fullscr='True',
    units="pix",
    color = 0
)

ls_stim = []
for i in ls_file:
#    print i
    mov = visual.MovieStim3(win, i, size=(1920, 1080),
        flipVert=False, flipHoriz=False, loop=False)
    ls_stim.append(mov)

novel_oddball = [3, 3, 3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
3, 9, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 
3, 3, 3, 3, 3, 9, 3, 3, 3, 9, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 3, 
3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 9, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 
3, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 9, 3, 3, 
3, 3, 9, 3, 3, 3, 3, 9, 3, 3, 9, 3, 3, 9, 3, 3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 3, 3, 
3, 9, 3, 3, 3, 3, 3, 9, 3, 3, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3, 
3, 3, 3, 3, 9, 3, 3, 3, 3, 3, 3, 9, 3, 3, 3]

control = [4, 5, 3, 6, 5, 7, 0, 3, 7, 6, 7, 1, 2, 6, 7, 0, 5, 0, 7, 0, 7, 3, 2, 1, 7, 0, 6, 1, 3, 1, 4, 6, 6, 5, 1, 4, 4, 5, 2, 3, 0, 5, 2, 3, 4, 2, 6, 5, 6, 6, 3, 7, 0, 1, 4, 6, 4, 0, 6, 6, 7, 4, 3, 6, 1, 1, 5, 4, 0, 4, 0, 2, 6, 2, 6, 7, 7, 7, 3, 0, 1, 7, 6, 1, 3, 2, 3, 5, 7, 0, 1, 5, 2, 3, 4, 2, 4, 6, 0, 4, 3, 2, 4, 1, 2, 0, 5, 1, 5, 3, 4, 6, 3, 5, 2, 2, 7, 1, 6, 0, 0, 5, 4, 0, 1, 5, 0, 3, 7, 5, 7, 4, 6, 2, 0, 0, 1, 1, 0, 5, 3, 2, 4, 7, 0, 7, 5, 2, 7, 1, 2, 7, 3, 0, 2, 3, 6, 2, 7, 3, 5, 3, 4, 5, 3, 7, 4, 2, 6, 6, 2, 1, 3, 1, 4, 5, 0, 2, 2, 6, 1, 4, 5, 1, 6, 3, 0, 5, 3, 2, 5, 4, 1, 7, 4, 4, 1, 5, 7, 1]

deviant_oddball = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 
1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 
1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 
1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 
1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 
1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1]


exp = np.array(control)

stim = ls_stim[exp[0]]
framerate=60 # Hz
duration = 0.5 # in sec
frame_num = int(duration*framerate)
trials = 200

core.wait(4.0)
if rec_flag==1:

    ser.write('3')

nov_stim_counter = -5

clock = core.Clock()
for idx, val in enumerate(exp):

    #clock.reset()
    if rec_flag==1:
        ser.write('1')
    core.wait(0.3)
#    t1 = clock.getTime()
#    print t1
    
#    while stim.status != visual.FINISHED:
#        stim.draw()
#        win.flip()
#    win.flip()
    for frameN in range(frame_num+1):
        stim.draw()
        win.flip()
    win.flip()
    
    stim.seek(0.01)
    if np.unique(exp).size > 3:
        isi = np.random.uniform(2.7, 3.2)
        # print 'control'
    else:
        isi = np.random.uniform(0.7, 1.2)
    core.wait(isi)
    
    if exp[idx+1] == 9:
        print nov_stim_counter
        nov_stim_counter = nov_stim_counter + 1
        stim = ls_stim[exp[idx+1] + nov_stim_counter]
    else:  
        # print exp[idx+1]
        stim = ls_stim[exp[idx+1]]
    
#scipy.misc.toimage(img_new, cmin=-1, cmax=1).save('outfile.jpg')
win.close()