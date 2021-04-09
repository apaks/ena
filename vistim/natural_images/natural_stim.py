from __future__ import division
import numpy as np
import scipy.misc
from PIL import Image
from psychopy import visual, core, event, filters
import serial
import math

rec_flag = 0
trials = 200
if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)
    trials = 20
    
myWin = visual.Window( [1920,1080], 
                        monitor="testMonitor", 
                        units="pix", 
                        screen=2, 
                        winType = 'pyglet',
                        colorSpace ='rgb',
                        fullscr = 'False',
                        
                       )
path = r"U:\Visual Stimulation\pak6\Vis Stim\natural_images\005.tif"


# this gives a (y, x) array of values between 0.0 and 255.0
img = Image.open(path)


maxsize = (1920, 1440)
# convert to grayscale
img = img.convert('L')
# resize to the fullscreen
img = img.resize(maxsize, Image.ANTIALIAS)
# convert to array
img = np.array(img)
# rescale to -1 +1
img = (img / 255.0) * 2.0 - 1.0
# invert image
img = np.flipud(img)
noise = (np.random.choice( [0,1], [img.shape[0], img.shape[1]])*2 -1)/2

# desired RMS
rms = 0.2
raw_img = img
# make the mean to be zero
raw_img = raw_img - np.mean(img)
# make the standard deviation to be 1
raw_img = raw_img / np.std(img)
# make the standard deviation to be the desired RMS
#raw_img = raw_img * rms

# convert to frequency domain
img_freq = np.fft.fft2(raw_img)

# calculate amplitude spectrum
img_amp = np.fft.fftshift(np.abs(img_freq))


#hp_filt = filters.butter2d_hp(
#    size=raw_img.shape,
#    cutoff=0.06,
#    n=10
#)
sf = 0.05
val = sf/12.0
hp_filt = filters.butter2d_hp(
    size=raw_img.shape,
    cutoff= val,
    n=10
)

img_filt = np.fft.fftshift(img_freq) * hp_filt


# convert back to an image
img_new = np.real(np.fft.ifft2(np.fft.ifftshift(img_filt)))

# generate phase scrambled image
img_fft = np.fft.fft2(raw_img)

img_amp = np.abs(img_fft) * np.fft.ifftshift(hp_filt)

img_phase = np.angle(np.fft.fft2(np.random.rand(*img.shape)))

scrambled_img = np.fft.ifft2(
    img_amp * np.cos(img_phase) +
    1j * (img_amp * np.sin(img_phase))
)

scrambled_img = np.real(scrambled_img)


scrambled_img = scrambled_img - np.mean(scrambled_img)
scrambled_img = scrambled_img / np.std(scrambled_img)
scrambled_img = np.clip(scrambled_img, a_min=-1.0, a_max=1.0)

# convert to mean zero and specified RMS contrast
img_new = img_new - np.mean(img_new)
img_new = img_new / np.std(img_new)
#img_new = img_new / img_new.max()


# there may be some stray values outside of the presentable range; convert < -1
# to -1 and > 1 to 1
img_new = np.clip(img_new, a_min=-1.0, a_max=1.0)
raw_img = np.clip(raw_img, a_min=-1.0, a_max=1.0)

stim = visual.ImageStim(
    win=myWin,
    image=scrambled_img,
    units="pix",
    size= (raw_img.shape[1],  raw_img.shape[0])
)

framerate=60 # Hz
duration = 1 # in sec
frame_num = int(duration*framerate)

if rec_flag==1:

    ser.write('3')
clock = core.Clock()
for i in range(1):
    print i
    if rec_flag==1:
        ser.write('1')
        
    core.wait(0.5)
    t1 = clock.getTime()  
    print t1
    for j in range(frame_num):
        
        #print j, sin_drift_noise[j][0][0]
        stim.draw()
        myWin.flip()
      
    
    core.wait(3)
    myWin.flip()
np.save('005_hp05_scrambled.npy', scrambled_img )    
myWin.close()