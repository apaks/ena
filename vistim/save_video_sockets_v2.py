# coding: utf-8

# Working acquisition of images through a camera using opencv
from pylab import array, plot, show, axis, arange, figure, uint8
import cv2
#import cv2.cv as cv
import numpy as np
import pickle
import socket
import datetime
import os, time
from instrumental.drivers.cameras import uc480

now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d_%H-%M-%S")

foldername =  'videos_' + str(date) 
os.makedirs(foldername)

#import PIL.ImageOps

#Coordinates of camera recording being displayed in the window?
#capture.set(3,320)
#capture.set(4,200)

#socket server
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8090)) #8089
serversocket.listen(5) # become a server socket, maximum 5 connections
connection, address = serversocket.accept()

#socket client
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8091)) #8089
print ("Connection is established")
counter = 1

while True:
    capture = cv2.VideoCapture(0)
    time.sleep(1.000)
    if capture.isOpened():
        print ("Cam is open")
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 120) 
        #Check obj analysis crop for changing x,y
        capture.set(cv2.CAP_PROP_FPS, 40)
        ###^Must match writer fps. Can increase to ~30 if needed
        ###CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras)

        
        buf = connection.recv(32) #32==max data size received from the connection
        print (buf.decode())
        #buf is data received over the socket connection from 'clientsocket.send()' in other program
        if len(buf) > 0: #If any data is received
            
            if buf == 'Finished': #IFF 'Finished' is received, stop video cap
                print (buf)
                cv2.destroyAllWindows()
                capture.release()
                break;
            cc =cv2.VideoWriter_fourcc(*'iYUV')
            #cc = cv2.cv.CV_FOURCC(*'iYUV')

            fname='video'+str(counter)+'.avi'
            fname = os.path.join(foldername, fname)

            writer = cv2.VideoWriter(filename=fname, fourcc = cc, ###Why use this encoding for video, exactly???
            #fourcc=cv.CV_FOURCC(*'X264'),
                                    fps=40, ######This is not always staying consistent w/rec time.
                                    frameSize=(160, 120)) # MUST MATCH CAPTURE
            #^Decreasing this size decreased speed necessary to record the frames.
            #frameSize=(1024, 640))

            print (buf, 'Recording video'+str(counter)+'.avi')
            print ('Proceeding')
            print ('Camera start at time:', datetime.datetime.now().time())
            clientsocket.send(b'Camera start') #Trigger stimulus on this message?
            #Keep this message just before frame numbers to improve synchrony

            for i in range(320): #total frames captured, captured at rate listed above (supposedly) (20 frames per second? 1/20 * 80 = 4.0s.  May not always be perfectly coordinated w recording time, but should be most of the time
                rval, frame = capture.read()
                
                
                frame=cv2.flip(frame, flipCode=0)
                #if counter >= 3:
                #    frame=cv2.flip(frame, flipCode=0)
                #^^^Currently inverts at vid 1, 3            

                writer.write(frame)

                #The feed appears darker than normal for some reason. The uc480 viewer has much better contrast.

                #cv2.imshow("input", frame)
                #frame = frame[y1:y1+height,x1:x1+width]
                #http://stackoverflow.com/questions/19363293/whats-the-fastest-way-to-increase-color-image-contrast-with-opencv-in-python-c
                image = frame.copy()
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (5,5), 3)
                retval, thresh = cv2.threshold(blur, 8, 255, cv2.THRESH_BINARY_INV)
                #Make a slider for Param1 of this!   ^^

                cv2.imshow("Preview", np.hstack([gray, thresh]))
                cv2.waitKey(1)

            print ('Camera stops at time:', datetime.datetime.now().time(), '\n')
            counter += 1
            writer.release()
            capture.release()
            
            """
            with open('video'+str(counter)+'_eye_pupil.pickle', 'wb') as handle:
                pickle.dump(data, handle)
            capture.release()
            """

#To make online analysis possible, a threshold slide bar has to be created from
#the appearance of the current frame from an indefinite VideoCapture. Once set so that 
#only the pupil and minor artifacts near the eye are present, then this could run well I think.
#Without this, the thresholding will be too inconsistent between mice and setups.
#How about try this in Object_Analysis_v2.py