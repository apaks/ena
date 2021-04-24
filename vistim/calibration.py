# -*- coding: utf-8 -*-

"""

Created on Mon Jun 29 10:34:16 2015



@author: jtrinity

"""



from psychopy import visual, core, event, monitors

import wx

import pickle

import matplotlib.pyplot as plt

import numpy



#myfit = psychopy.monitors.GammaCalculator(inputs=[], lums=[])

#print myfit.params







#get monitor settings from wx

app = wx.App(False)

wx_res  = wx.GetDisplaySize()

wx_PPI = wx.ScreenDC().GetPPI()







#user variables

spatial_frequency = 0.05

monitor_distance = 20

monitor_width = 2.54 * wx_res[0]/wx_PPI[0]

#monitor_width = 37.5



horiz_res = wx_res[0]

vert_res = wx_res[1]

#horiz_res = 1920

#vert_res = 1280



print wx_res, wx_PPI, monitor_width



#setup monitor

mon = monitors.Monitor("mymon", distance = monitor_distance, width = monitor_width)

mon.currentCalib['sizePix'] = [horiz_res, vert_res]

mon.saveMon()



#setup window

mywin = visual.Window([horiz_res,vert_res], monitor = mon, fullscr = False,units = "deg", screen=2)

print mywin.monitor.currentCalib



grating = visual.GratingStim(tex = "sin",win=mywin, mask="circle", size=300, pos=[0,0], sf=spatial_frequency)



flat_color = visual.GratingStim(win=mywin, size=300, pos=[0,0], sf=0, colorSpace ='rgb255', color=(255,255,255))

gray = visual.GratingStim(win=mywin, size=300, pos=[0,0], sf=0, colorSpace ='rgb255', color=(127,127,127))



#A couple of functions for testing your monitor.

def runGrating():

    while True:

        grating.setPhase(0,'+')

        grating.draw()

        mywin.flip()

        

        if len(event.getKeys())>0: break

        event.clearEvents()

        

    gray.draw()

    mywin.flip()

    event.waitKeys()  

    event.clearEvents()

        

    while True:

        grating.setPhase(0,'+')

        grating.setTex("sqr")

        grating.draw()

        mywin.flip()

        

        if len(event.getKeys())>0: break

        event.clearEvents()

        

#shows a series of grayscale intenisty slides for manual monitor calibration

def presentGrayscale():

    inputs = []

    lums = []

    flat_color.draw()

    mywin.flip()

    event.waitKeys()

    mywin.flip()

    flat_color.color -= (255,255,255)

    event.waitKeys()

    while flat_color.color[0] <= 255:

        inputs.append(flat_color.color[0])

        flat_color.draw()

        mywin.flip()

        event.waitKeys()       

        try:

            x = getValue(message = "Luminance: ")

            lums.append(float(x))

            print flat_color.color[0], x

        except ValueError, e:

            print "error", e, "entering 0 instead."

            lums.append(0.0)

        flat_color.color += (15,15,15)

        mywin.flip()

        



    return inputs, lums



#basic input dialog; used in presentGrayscale       

def getValue(parent = None, message ='', default_value =''):

    dlg = wx.TextEntryDialog(parent, message, defaultValue=default_value)

    dlg.ShowModal()

    result = dlg.GetValue()

    dlg.Destroy()

    return result



#presents intensity slides and pickles output

def calibrateMonitor():

    calibrations = presentGrayscale()



    output = open('last_calibration.pkl', 'wb')

    pickle.dump(calibrations, output)

    output.close()

    

    return calibrations







#sets gamma of selected monitor to last calibration

def setGamma():

    pkl_file = open('last_calibration.pkl', 'rb')

    calibrations = pickle.load(pkl_file)

    levels = calibrations[0]

    lums_i = calibrations[1]

    lums = numpy.array([lums_i,lums_i,lums_i,lums_i])

    print lums[0,0]

    

    

    print levels, lums

    #simple calculate gamma

    myfit = monitors.GammaCalculator(inputs=calibrations[0], lums = calibrations[1])

    gamma_exp = myfit.gamma

    print gamma_exp

    

    #monitor center style

    mon.setLumsPre(lums)

    mon.setLevelsPre(levels)

    linMethod = mon.getLinearizeMethod()

    currentCal = mon.currentCalib['gammaGrid']

    print currentCal

    if linMethod==4:

        currentCal = numpy.ones([4,6],'f')*numpy.nan

        for gun in [0,1,2,3]:

            gamCalc = monitors.GammaCalculator(levels, lums[gun,:], eq=linMethod)

            currentCal[gun,0]=gamCalc.min#min

            currentCal[gun,1]=gamCalc.max#max

            currentCal[gun,2]=gamCalc.gamma#gamma

            currentCal[gun,3]=gamCalc.a#gamma

            currentCal[gun,4]=gamCalc.b#gamma

            currentCal[gun,5]=gamCalc.k#gamma

    else:

        currentCal = numpy.ones([4,3],'f')*numpy.nan

        for gun in [0,1,2,3]:

            gamCalc = monitors.GammaCalculator(levels, lums, eq=linMethod)

            currentCal[gun,0]=lums[gun,0]#min

            currentCal[gun,1]=lums[gun,-1]#max

            currentCal[gun,2]=gamCalc.gamma#gamma

     

    mon.setGammaGrid(currentCal)

    mon.saveMon()

    print mon.currentCalib

    

    pkl_file.close()



def manualCalibration():



    #calibrations = calibrateMonitor()

    setGamma()

#    plt.plot(calibrations[0],calibrations[1])
#
#    plt.show()

    

#

manualCalibration()

#event.waitKeys()

runGrating()



mywin.close()

core.quit()

