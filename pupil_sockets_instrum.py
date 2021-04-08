# @ Alex Pak. 2021
# _v1
# save pupil videos using sockets and instumental
import cv2
import numpy as np
import socket
import time, os, datetime
from instrumental.drivers.cameras import uc480

now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d_%H-%M-%S")

foldername =  'videos_' + str(date) 
os.makedirs(foldername)

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

duration = 3 #in s
instruments = uc480.list_instruments()
cam = uc480.UC480_Camera(instruments[0])

width, height = 200, 200
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fourcc =cv2.VideoWriter_fourcc(*'iYUV')
# fourcc = cv2.VideoWriter_fourcc(*'iYUV')
# fourcc = cv2.VideoWriter_fourcc(*'DIVX')
fourcc = cv2.VideoWriter_fourcc(*'PIM1')
total_frames = 180 # in frames with 60fps

ls_frames = []
# print(cam.DEFAULT_KWDS)
# frame = cam.latest_frame(copy = True)
# print(frame.shape)
counter = 0
while True:
    buf = connection.recv(32) #32==max data size received from the connection
    print (buf.decode())
    if len(buf) > 0:
        if buf.decode() == 'Finished': #IFF 'Finished' is received, stop video cap
            cv2.destroyAllWindows()
            cam.close()
            break
        ls_frames = []
        cam.start_live_video(framerate = "60 Hz", exposure_time = "16 ms", 
                                    width = width, height = height, top = 0, left = 0)
        print (cam.is_open, cam.framerate)

        fname='video'+str(counter)+'.avi'
        fname = os.path.join(foldername, fname)


        print (f"Recording {fname}")
        print ('Camera start at time:', datetime.datetime.now().time())
        clientsocket.send(b'Camera start') #Trigger stimulus on this message?

        # since = time.time()
        t_end = time.time() + duration
        while time.time() < t_end:
        # while (i < total_frames):
            flag = cam.wait_for_frame(timeout = "0 ms")
            if flag:
                # time.sleep(0.1)
                frame = cam.latest_frame(copy = True)
                # frame = cv2.flip(frame, 0)
                frame = frame.astype('uint8')
                ls_frames.append(frame)
                # frame = cv2.flip(frame, flipCode= 1)
                # print(frame.shape)
                # shape should be reversed, eg. flip frame
                img = frame.copy()
                blur = cv2.GaussianBlur(img, (5,5), 3)
                retval, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY_INV)
                cv2.imshow('Preview', np.hstack([img, thresh]))
                cv2.waitKey(1)
                # Display the resulting frame
        
        
        out = cv2.VideoWriter(fname, fourcc, 60.0, (height, width), False)
        for img in ls_frames:
            out.write(img)
        out.release()
        cam.stop_live_video()
        print ('Camera stops at time:', datetime.datetime.now().time(), '\n')
        print(f"Number of frames: {len(ls_frames)}")
        counter = counter + 1
        
# end = time.time()
# print(f"Finished in {end-since}")
# When everything done, release the capture
cv2.destroyAllWindows()
cam.close()