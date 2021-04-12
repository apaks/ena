# Alex Pak, 2017 
# generate spatilly filtered noise vis stims, for sf experiments 

from __future__ import division
import numpy as np
import scipy.misc
import psychopy.visual
import psychopy.event
from psychopy.visual import filters
import wx


app = wx.App(False)
wx_res  = wx.GetDisplaySize()
wx_PPI = wx.ScreenDC().GetPPI()

monitor_distance = 17 # cm

monitor_width = 2.54 * wx_res[0]/wx_PPI[0] # convert inch to cm

win = psychopy.visual.Window(
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
    
def fft_noise():
    
#filteredNoise = makeFilteredNoise(1024, 0.001)
    noise = (np.random.rand( 2048, 2048)*2 -1)/2  # generate noise matrix, rescale to -1,1
    #raw_img = noise
    # we first need to convert it to the -1:+1 range
    #raw_img = (raw_img / 255.0) * 2.0 - 1.0
    #
    # we also need to flip it upside-down to match the psychopy convention
    raw_img = np.flipud(noise)

    # make the mean to be zero
    raw_img = raw_img - np.mean(raw_img)
    # make the standard deviation to be 1
    raw_img = raw_img / np.std(raw_img)
    # make the standard deviation to be the desired RMS

    # convert to frequency domain
    img_freq = np.fft.fft2(raw_img)
    # calculate amplitude spectrum
    img_amp = np.fft.fftshift(np.abs(img_freq))
    return raw_img, img_amp, img_freq
#lp_filt = filters.butter2d_lp(
#    size=raw_img.shape,
#    cutoff=0.02,
#    n=10
#)
#
#img_filt = np.fft.fftshift(img_freq) * lp_filt


#hp_filt = psychopy.filters.butter2d_hp(
#    size=raw_img.shape,
#    cutoff=0.05,
#    n=10
#)
#
#img_filt = np.fft.fftshift(img_freq) * hp_filt

# all calculations below only apply for 1920x1920 matrix and the ViewSonic monito (width 40 cm) 

bp_step = 0.00003 # 0.00639 step in sf on screen
max_sf = wx_res[0]/monitor_width # for 1920x1080 res on 40 cm screen width, not sure about this need validation
sf_scr = [ 0.01,   0.02,   0.04, 0.08, 0.16, 0.32 ] 


stims = 30
#stims_3d = np.zeros((stims,noise.shape[0], noise.shape[1] ))
stims_3d_norm = np.zeros((stims,1080, 1920 ))
for j in range(3):
    raw_img, img_amp, img_freq = fft_noise()
    
    x = 0.04*180/(max_sf*monitor_distance*np.pi)
    bp_filt = filters.butter2d_bp(
        size=raw_img.shape,
        cutin = x,
        cutoff= x + bp_step ,
        n=10
    )
    sf_obs = [max_sf*x*monitor_distance*np.pi/180 , max_sf*monitor_distance*np.pi/180*(x+bp_step)]
    print sf_obs
    
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
    stims_3d_norm[j,:,:] = np.clip(img_new, a_min=-1.0, a_max=1.0)
    # to -1 and > 1 to 1
    
# generate stim with two sf bands
#test_img = stims_3d_norm[0]
#test_img = test_img - np.mean(test_img)
#test_img = test_img / np.std(test_img)
#test_img = test_img/ test_img.max()
#test_img = np.clip(test_img, a_min=-1.0, a_max=1.0)


framerate=60 # Hz
duration = 1 # in sec
frame_num = int(duration*framerate)
temporal_frequency = 1
#sin_drift_noise = np.zeros((frame_num,test_img.shape[0], test_img.shape[1] ), dtype='float32')

#sin_drift_noise=[]
#sin_drift_noise.append(test_img)
#starting_phase=np.arcsin(test_img)
#phase_shift=2*np.pi/framerate
#
#for i in range(frame_num):
#    
#    starting_phase=starting_phase+phase_shift
#    new_frame=np.sin(temporal_frequency*(starting_phase))
#    sin_drift_noise[i] = new_frame
    #sin_drift_noise.append(new_frame)
    
img = psychopy.visual.GratingStim(
    win=win,
    tex = stims_3d_norm[0],
    units = "pix",
#    ori = 0,
    size = (1920, 1080),
#    mask = 'gauss' 
)
for i in range(stims_3d_norm.shape[0]):
    for j in range(frame_num):
        img.tex = stims_3d_norm[i]
#        img.setPhase((0.033, 0), '+')
        #print j, sin_drift_noise[j][0][0]
        img.draw()
        win.flip()
    print i
    #img.draw()
    win.flip()
#for j in range(1,6):
#    np.save(str(j) + 'bp_noise.npy', stims_3d_norm[j-1] )
#np.save('sf_filt_noise_vmmn.npy', stims_3d_norm )

psychopy.event.waitKeys()

#scipy.misc.toimage(img_new, cmin=-1, cmax=1).save('outfile.jpg')
win.close()