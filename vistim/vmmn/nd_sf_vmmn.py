# Alex Pak, 2017 
# MMN paradigm by using bp filtered 
# noise in particular sf, using local deviant or omission

from __future__ import division
from psychopy import visual, core, event
import numpy as np
import scipy.misc
import wx, sys
import serial, pickle, socket
import datetime
from subprocess import Popen

rec_flag = 1
speed_flag = 0
ppl_flag = 0
opto_flag = 1

if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)

if opto_flag==1:
    opto_ser=serial.Serial("COM15", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)
    
if speed_flag == 1:
    ser_speed = serial.Serial("COM8", baudrate=9600) 
    #ser_speed = serial.Serial("COM8", baudrate=115200) # 12/14/2018 important change. make sure the speed of arduino serial is the same as here
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename =  'speed_' + str(date) + '.pkl'
    print filename
    output = open(filename, 'wb')
    ser_speed.write('3')
    
if ppl_flag == 1:
    script = r"C:\Users\Achub_Lab\Desktop\Vis Stim\Save_video_sockets_G-1-G---G (Drifting)_Pupillometry.py"
    theproc = Popen(["python", script])
    core.wait(0.5)
    
path = r"C:\Users\Achub_Lab\Desktop\Vis Stim\vmmn_paradigms\sf04_filt_noise_vmmn.npy"
imgs = np.load(path)

win = visual.Window(
    monitor = 'mymon',
    size= [1920,1080],
    screen=1,
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

opto_seq = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
       1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
       0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0,
       0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
       0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0,
       0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
       0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
       1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0,
       0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
       0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
       0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1,
       0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
       0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
       0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0,
       0, 0, 0, 0])

deviant_oddball = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 
1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 
1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 
1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 
1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 
1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1]

loc_omission = [3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 
40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 
3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 
3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 
3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 
3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 
3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40, 3, 
3, 3, 3, 3, 3, 3, 40, 3, 3, 3, 3, 3, 3, 3, 40]

opto_idx = ([24, 25, 62, 63, 84, 84, 85, 85, 118, 119, 143, 144, 150, 151, 161, 162, 172, 172, 173, 173, 190, 190, 191, 191, 198, 199, 220, 221, 238, 239, 241, 242, 289, 289, 290, 290, 303, 304, 316, 317, 324, 325, 328, 329, 339, 340, 344, 345, 362, 363])

novel_oddball = np.array(novel_oddball)
deviant_oddball = np.array(deviant_oddball)
loc_omission = np.array(loc_omission)

exp = opto_seq

stim = visual.ImageStim(win, 
    image = imgs[exp[0]], # change this to sf stim 
    units="pix", 
    size=(imgs[0].shape[1], imgs[0].shape[0]))
    
framerate=60 # Hz
duration = 0.5 # in sec
frame_num = int(duration*framerate)
trials = 200

if ppl_flag == 1:

    #Sockets client
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8090))#8089

    print 'Stimuli listen ready\n';
    sys.stdout.flush();

    #Sockets server
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 8091)) #8089
    serversocket.listen(5) # become a server socket, maximum 5 connections
    connection, address = serversocket.accept()

core.wait(4.0)
if rec_flag==1:

    ser.write('3')
    
tmp = 0
clock = core.Clock()
for idx, val in enumerate(exp):
    
    stim.opacity = 1
    #clock.reset()

    if exp[idx] == 40: 
        stim.opacity = 0
    if ppl_flag == 1:  
        clientsocket.send('Hi there!') #This message triggers opening of video cap & rec start
   
        buff = connection.recv(32)
    else:
        buff = '1'
       
    if len(buff) > 0:
        if speed_flag ==1:    
            ser_speed.write('1')
        if rec_flag==1:
            ser.write('1')
        if opto_flag==1:
            if idx in opto_idx:
                opto_ser.write('1')
        #        t1 = clock.getTime()
        #        print tmp - t1
        #        tmp = t1

        core.wait(0.3)

        #    print t1
        for j in range(frame_num):
            #print j, sin_drift_noise[j][0][0]
            stim.draw()
            win.flip()
        #        break
        #        t2 = clock.getTime()
        #        print t2-t1 
        win.flip()
        isi = np.random.uniform(0.2, 0.7)

        if exp[idx+1] == 1:
            stim_idx = np.random.choice(np.arange(2,25))
            stim.image = imgs[stim_idx]
        elif exp[idx+1] == 40:
            print 'omis'
            isi = 1.2
        else:
            stim.image = imgs[exp[idx+1]]
        core.wait(isi)

        if speed_flag ==1:
            ser_speed.write('2')
            x2 = ser_speed.readline()
            print x2
            try:
                pickle.dump(x2, output)
            except:
                print ('data not written')
        #######Speed#######
        core.wait(0.2)#THis was added as a safety (after FX data set) 
    
output.close()    
clientsocket.send('Finished')
#scipy.misc.toimage(img_new, cmin=-1, cmax=1).save('outfile.jpg')
win.close()