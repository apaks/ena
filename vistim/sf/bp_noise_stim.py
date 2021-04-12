# Alex Pak, 2017 present vis stim from .npy files
import numpy as np
from psychopy import visual, event, filters, core
import scipy.misc

sf_prandom_seq = [1, 4, 0, 3, 3, 1, 2, 1, 1, 2, 1, 2, 2, 3, 0, 4, 4, 4, 
1, 2, 3, 2, 4, 4, 0, 0, 3, 0, 3, 0, 1, 2, 1, 4, 0, 3, 3, 4, 1, 4, 2, 
1, 2, 1, 1, 1, 1, 0, 1, 2, 2, 1, 4, 3, 2, 0, 0, 4, 0, 2, 0, 0, 4, 2, 
1, 2, 4, 2, 3, 2, 0, 1, 3, 4, 0, 0, 3, 4, 3, 0, 3, 0, 2, 3, 3, 4, 3, 
3, 4, 4, 2, 0, 1, 1, 3, 4, 0, 3, 4, 2]

#path = r"U:\Visual Stimulation\pak6\Vis Stim\bp_noise_all.npy"
path = r"U:\Visual Stimulation\pak6\Vis Stim\bp_noise_prime_3-13_sf.npy"
imgs = np.load(path)
print imgs.shape
#noise = np.random.random([512, 512])*2-1

win = visual.Window([1920,1080], 
    monitor='mymon', screen=1)
    
stim = visual.ImageStim(win, 
    image = imgs[0], 
    units="pix", 
    size=imgs[0].shape)
    
duration = 2 # in sec
frames = int(60*duration)

for j in range(imgs.shape[0]):
    stim.image = imgs[j]
    for i in range(frames):
    
        stim.draw()
        win.flip()
    
    win.flip()
    core.wait(3)
    
#event.waitKeys()

