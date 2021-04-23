# Alex Pak, 2017 
# MMN paradigm by using bp filtered 
# noise in particular sf, using local deviant or omission

from __future__ import division
import numpy as np
import scipy.misc
from psychopy import visual, core, event
from psychopy.visual import filters
import wx
import serial

rec_flag = 0
if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)
 
path = r"U:\Visual Stimulation\pak6\Vis Stim\vmmn_paradigms\sf04_filt_noise_vmmn.npy"
imgs = np.load(path)

win = visual.Window(
    monitor = 'mymon',
    size= [1920,1080],
    screen=2,
    fullscr='True',
    units="pix",
    color = 0
)


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

novel_oddball = np.array(novel_oddball)
control = np.array(control)
deviant_oddball = np.array(deviant_oddball)

exp = control

def add_tf(test_img):
    
    temporal_frequency = 2
    frame_num = 30
    framerate = 60
    tf_stim = np.zeros((frame_num,test_img.shape[0], test_img.shape[1] ), dtype='float32')

    #sin_drift_noise=[]
    #sin_drift_noise.append(test_img)
    starting_phase=np.arcsin(test_img)
    phase_shift=2*np.pi/framerate

    for i in range(frame_num):
        
        new_frame=np.sin(temporal_frequency*(phase_shift)+starting_phase)
        tf_stim[i] = new_frame
        starting_phase = temporal_frequency*(phase_shift)+starting_phase 
        #sin_drift_noise.append(new_frame)
        
    #win.recordFrameIntervals = True
    ls = []
    for i in range(frame_num):
        img = visual.ImageStim(
            win=win,
            colorSpace = 'rgb',
            image = tf_stim[i],
            units="pix",
            #mask = 'gauss',
            size = (test_img.shape[1], test_img.shape[0] )
            
        )
        ls.append(img)
    return ls

stim = add_tf(imgs[0])
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
    for j in range(frame_num):
        #print j, sin_drift_noise[j][0][0]
        stim[j].draw()
        win.flip()
        win.getMovieFrame()
    win.flip()
#    win.getMovieFrame()
    win.saveMovieFrames(fileName='sf_tf_1.mp4', fps = 60)
    
    isi = np.random.uniform(0.7, 1.2)
    core.wait(isi)
    break
#    if exp[idx+1] == 9:
#        print nov_stim_counter
#        nov_stim_counter = nov_stim_counter + 1
#        stim.image = imgs[exp[idx+1] + nov_stim_counter]
#    else:
#        stim.image = imgs[exp[idx+1]]
    
#scipy.misc.toimage(img_new, cmin=-1, cmax=1).save('outfile.jpg')
win.close()