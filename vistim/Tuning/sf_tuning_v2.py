# Alex Pak, 2018 
# sf - 0.01, 0.02, 0.04, 0.08, 0.16, 0.32 cyc/deg
# each stim will be generated from bp filtering random noise
# Arduino set 1s each trial
# total time for rec = 5*120 = 600 s

from __future__ import division
from psychopy import visual, event, filters, core
import numpy as np
import scipy.misc
import serial
from random import randint
import datetime
import wx

rec_flag = 1
opto_flag = 0

if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)

if opto_flag==1:
    opto_ser=serial.Serial("COM15", baudrate=9600)

app = wx.App(False)
wx_res  = wx.GetDisplaySize()
wx_PPI = wx.ScreenDC().GetPPI()

monitor_distance = 17 # cm

monitor_width = 2.54 * wx_res[0]/wx_PPI[0] # convert inch to cm

def fft_noise():
    noise = (np.random.rand( 2048, 2048)*2 -1)/2  # generate noise matrix, rescale to -1,1
    # we first need to convert it to the -1:+1 range
    # we also need to flip it upside-down to match the psychopy convention
    raw_img = np.flipud(noise)
    # make the mean to be zero
    raw_img = raw_img - np.mean(raw_img)
    # make the standard deviation to be 1
    raw_img = raw_img / np.std(raw_img)
    # convert to frequency domain
    img_freq = np.fft.fft2(raw_img)
    # calculate amplitude spectrum
    img_amp = np.fft.fftshift(np.abs(img_freq))
    return raw_img, img_amp, img_freq

bp_step = 0.00003 # 0.00639 step in sf on screen
max_sf = wx_res[0]/monitor_width # for 1920x1080 res on 40 cm screen width, not sure about this need validation
def make_sf_stim(sf_target):
    raw_img, img_amp, img_freq = fft_noise()
    x = sf_target*180/(max_sf*monitor_distance*np.pi)
    bp_filt = filters.butter2d_bp(
        size=raw_img.shape,
        cutin = x,
        cutoff= x + bp_step ,
        n=10
    )
    img_filt = np.fft.fftshift(img_freq) * bp_filt
    # convert back to an image
    img_new = np.real(np.fft.ifft2(np.fft.ifftshift(img_filt)))
    #stims_3d[j,:,:] = img_new
    # convert to mean zero and specified RMS contrast
    img_new = img_new[:1080, :1920]
    img_new = img_new - np.mean(img_new)
    img_new = img_new / np.std(img_new)
    img_new = img_new /img_new.max()
    # there may be some stray values outside of the presentable range; convert < -1
    img_new = np.clip(img_new, a_min=-1.0, a_max=1.0)
    return img_new

win = visual.Window(
    monitor = 'mymon',
    size= [1920,1080],
    screen = 1,
    fullscr='True',
    units="pix",
    color = 0
)
    

    
sf_seq = [2, 0, 0, 4, 3, 3, 0, 4, 4, 3, 2, 5, 3, 2, 0, 4, 1, 0, 5, 2, 0, 
1, 0, 1, 3, 5, 2, 5, 1, 2, 0, 5, 2, 3, 5, 1, 0, 4, 3, 2, 5, 5, 3, 5, 
2, 0, 3, 3, 0, 3, 4, 5, 4, 1, 4, 0, 1, 5, 4, 1, 5, 3, 3, 5, 3, 3, 2, 
3, 2, 1, 1, 5, 1, 4, 1, 2, 3, 2, 4, 2, 1, 0, 5, 5, 2, 2, 4, 1, 4, 1, 
3, 1, 0, 4, 4, 4, 4, 0, 5, 4, 4, 0, 3, 5, 5, 2, 1, 3, 4, 1, 5, 0, 2, 
2, 0, 0, 0, 1, 2, 1]

opto_seq = np.array([4, 4, 3, 5, 0, 5, 3, 1, 2, 3, 5, 3, 0, 1, 0, 3, 2, 4, 5, 5, 0, 0,
       5, 1, 3, 4, 4, 4, 5, 1, 2, 1, 4, 5, 3, 1, 4, 0, 0, 3, 0, 2, 0, 1,
       3, 1, 0, 5, 5, 2, 1, 1, 1, 4, 4, 1, 5, 0, 5, 3, 1, 3, 0, 3, 0, 3,
       3, 2, 4, 1, 5, 2, 5, 3, 5, 5, 0, 0, 3, 5, 4, 3, 0, 2, 1, 5, 0, 4,
       5, 0, 3, 2, 3, 4, 5, 0, 4, 0, 2, 2, 4, 3, 5, 4, 1, 2, 1, 1, 2, 3,
       2, 2, 0, 3, 0, 1, 2, 5, 2, 3, 0, 1, 3, 4, 0, 2, 2, 2, 0, 5, 4, 2,
       3, 2, 3, 3, 4, 0, 4, 3, 3, 1, 5, 2, 0, 2, 5, 3, 2, 5, 5, 4, 1, 3,
       4, 3, 1, 0, 2, 2, 5, 4, 1, 3, 1, 1, 4, 4, 1, 5, 3, 3, 5, 4, 3, 3,
       1, 0, 2, 4, 1, 5, 1, 3, 5, 1, 1, 1, 4, 2, 3, 0, 0, 1, 1, 1, 3, 2,
       1, 4, 4, 3, 2, 3, 4, 5, 4, 5, 3, 1, 2, 1, 2, 2, 0, 5, 0, 2, 4, 4,
       2, 5, 4, 0, 5, 0, 4, 4, 3, 0, 2, 5, 5, 3, 0, 4, 1, 3, 0, 0, 1, 2,
       2, 5, 1, 4, 3, 0, 0, 5, 4, 4, 1, 0, 4, 2, 2, 4, 5, 1, 5, 0, 5, 2,
       2, 0, 2, 2, 2, 0, 1, 4, 4, 1, 5, 4, 4, 0, 2, 5, 5, 0, 0, 1, 3, 0,
       1, 3, 5, 5, 4, 1, 0, 2, 2, 2, 3, 5, 1, 4])

opto_idx = np.array([0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1,
       1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0,
       0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1,
       1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1,
       1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0,
       0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1,
       0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1,
       1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1,
       1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
       1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1,
       0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1,
       1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0,
       0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0,
       1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0])

sf_list = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]
stim_duration = 0.5 # in sec
frame_rate = 60.0
tf = 0
frames = int(frame_rate*stim_duration)
ls = []
core.wait(4)
if rec_flag==1:
    ser.write('3')
    #ser2.write('3')
    
clock = core.Clock()
#win.recordFrameIntervals = True
print 'Experiment starts at:', datetime.datetime.now().time()
for idx, val in enumerate(sf_seq):
    if idx%40 == 0:
        print 'trial', idx, 'sf =', val
#    val = 2
    stim1 = make_sf_stim(sf_list[val])
    img = visual.GratingStim(
        win=win,
        tex = stim1,
        units="pix",
        #mask = 'gauss',
        size = (1920, 1080),
    )

    if rec_flag==1:
        ser.write('1')
        #ser2.write('1')
#    t1 = clock.getTime()
    if opto_flag==1:
        if opto_idx[idx] == 1:
            opto_ser.write('1')
    core.wait(0.3)

    for l in range(frames):
        img.draw()
        win.flip()
#        break
#    t2 = clock.getTime()
#    ls.append(t2 - t1)   
#    print t2-t1
#    win.getMovieFrame()
#    win.saveMovieFrames(fileName='sf-03_v3.png')  
    win.flip()

    rint = randint(1,3)
    core.wait(rint)

#event.waitKeys()

