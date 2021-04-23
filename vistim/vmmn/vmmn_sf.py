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

app = wx.App(False)
wx_res  = wx.GetDisplaySize()
wx_PPI = wx.ScreenDC().GetPPI()

monitor_distance = 17 # cm

monitor_width = 2.54 * wx_res[0]/wx_PPI[0] # convert inch to cm

win = visual.Window(
    monitor = 'mymon',
    size= [1920,1080],
    screen=2,
    fullscr='True',
    units="pix",
    color = 0
)

# this gives a (y, x) array of values between 0.0 and 255.0
#raw_img = scipy.misc.imread(
#    "unsw_bw.jpg",
#    flatten=True
#)


def makeFilteredNoise(res, radius, shape='gauss'):
    noise = np.random.random([res, res])
    kernel = filters.makeMask(res, shape=shape, radius=radius)
    filteredNoise = filters.conv2d(kernel, noise)
    filteredNoise = (filteredNoise-filteredNoise.min())/(filteredNoise.max()-filteredNoise.min())*2-1
    return filteredNoise
 
def make_sf_stim(raw_img, sf_target):
    x = (sf_target/100)*180/(max_sf*monitor_distance*np.pi)
    bp_filt = filters.butter2d_bp(
        size=raw_img.shape,
        cutin = x,
        cutoff= x + bp_step ,
        n=10
    )
    # make the mean to be zero
    raw_img = raw_img - np.mean(raw_img)
    # make the standard deviation to be 1
    raw_img = raw_img / np.std(raw_img)
    # make the standard deviation to be the desired RMS

    # convert to frequency domain
    img_freq = np.fft.fft2(raw_img)

    # calculate amplitude spectrum
    img_amp = np.fft.fftshift(np.abs(img_freq))
    #stims_3d = np.zeros((stims,noise.shape[0], noise.shape[1] ))
    stims_3d_norm = np.zeros((noise.shape[0], noise.shape[1] ))

    sf_obs = [max_sf*x*monitor_distance*np.pi/180 , max_sf*monitor_distance*np.pi/180*(x+bp_step)]
    #print sf_obs
    img_filt = np.fft.fftshift(img_freq) * bp_filt

    # convert back to an image
    img_new = np.real(np.fft.ifft2(np.fft.ifftshift(img_filt)))
    #stims_3d[j,:,:] = img_new
    # convert to mean zero and specified RMS contrast
    img_new = img_new - np.mean(img_new)
    img_new = img_new / np.std(img_new)
    img_new = img_new /img_new.max()


    # there may be some stray values outside of the presentable range; convert < -1
    stims_3d_norm = np.clip(img_new, a_min=-1.0, a_max=1.0)
    # to -1 and > 1 to 1
    return stims_3d_norm
    

exp_omission = [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 
0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 
1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 
1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 
1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 
1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 
1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 
1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0]


full_control = [2, 2, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 
2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 
2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 
2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 
2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 
2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1]

loc_oddball = [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 
2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 
1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 
1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 
1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 
1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 
1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 
1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2]

glob_oddball = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 
1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 
1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 
1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 
1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 
1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1]


exp = control
# all calculations below only apply for 1920x1920 matrix and the ViewSonic monito (width 40 cm) 
x = 0.0035
bp_step = 0.00003 # 0.00639 step in sf on screen
max_sf = wx_res[0]/monitor_width 
# for 1920x1920 res on 40 cm screen width, not sure baout this need validation

framerate=60 # Hz
duration = 0.5 # in sec
frame_num = int(duration*framerate)
trials = 200

# make redundant stim
noise = (np.random.choice( [0,1], [2048, 2048])*2 -1)/2  # generate noise matrix, rescale to -1,1
raw_img = np.flipud(noise)
tmp = make_sf_stim(raw_img)


ISI = core.StaticPeriod(screenHz=60)
if rec_flag==1:

    ser.write('3')

clock = core.Clock()
for i in range(len(exp)):
    print i
    #clock.reset()
    
    
    ISI.start(2)  # start a period of 0.5s
    
    if exp[i] == 2:
        #filteredNoise = makeFilteredNoise(1024, 0.001)
        noise = (np.random.choice( [0,1], [2048, 2048])*2 -1)/2  # generate noise matrix, rescale to -1,1
        raw_img = np.flipud(noise)
        stim1 = make_sf_stim(raw_img, 4)
    elif exp[i] == 0:
        stim1 = tmp*0
    else:
        stim1 = tmp
    img = visual.ImageStim(
        win=win,
        image = stim1,
        units="pix",
        #mask = 'gauss',
        size = np.shape(stim1)
    )
    ISI.complete()  # finish the 0.5s, taking into account one 60Hz frame
    
    if rec_flag==1:
        ser.write('1')
    core.wait(0.3)
    #t1 = clock.getTime()
    #print t1
    for j in range(frame_num):
        #print j, sin_drift_noise[j][0][0]
        img.draw()
        win.flip()
    win.flip()
    #core.wait(2)
#    np.save(str(j) + 'bp_noise.npy', stims_3d_norm[j-1] )
#np.save('tf_stim_bp_noise_sf42.npy', test_img )



#scipy.misc.toimage(img_new, cmin=-1, cmax=1).save('outfile.jpg')
win.close()