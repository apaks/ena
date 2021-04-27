# Alex Chubykin, 2012, Sam Kissinger 2015, Alex Pak 2016


from psychopy import visual, core #import some libraries from PsychoPy
#import socket #for connecting to other programs
import sys
import datetime
import time
from random import randint
import pickle
import serial
connected=False
ser=serial.Serial("COM6", baudrate=9600)
ser1=serial.Serial("COM11", baudrate=9600)

#Create a window
mywin = visual.Window( [1920,1080], 
                        monitor="mymon", 
                        units="deg", 
                        screen=1, 
                        winType = 'pyglet',
                        colorSpace ='rgb',
                        color=0)

#Create some stimuli



#Draw the stimuli and update the window - example

now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d_%H-%M-%S")



filename =  'lick_times_' + str(date) + '.pkl'
print filename


mywin.flip()


core.wait(4.0)
ser.write('3')

'''
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

#Stim/window prep
fixation.draw() #Draw gray screen now to eliminate future processing time?
mywin.update()

core.wait(4.0)
ser.write('3')
'''
#Cycling of stimulus
#while 1: #Infinite stimulus repeat
for ii in range(200): #number of recordings
#    clientsocket.send('Hi there!') #This message triggers opening of video cap & rec start
#    print 'Sent', ii+1
    #DataValue=ser.read()
    ser1.write('3')
    
    x =ser1.readline()
    
    print x
    
    
    try:
        output = open(filename, 'wb')
        pickle.dump(x, output)
        output.close()
    except:
        print ('data not written')

     
    tick = 6
    while(1):
   
        ser1.write('5')
         
        flag = ser1.readline()
         
        
        if flag[0]=='t':
           tick = tick + 1
        if tick>5:
            ser.write('1')
            core.wait(1)
            break
                
    print tick

        
 
     
    r = randint(3,6)
     #print r
    core.wait(r)#this wait = 7.7 instead of 7.  Accounts for the 0.5s after stim #1, and 200ms of stim2
#        print 'Cycle ends at: ', datetime.datetime.now().time(), '\n'


#clientsocket.send('Finished')