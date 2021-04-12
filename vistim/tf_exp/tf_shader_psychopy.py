# From Psychopy 2017, study tf

from __future__ import division
import numpy as np
from psychopy import visual, event,core
import serial

core.checkPygletDuringWait = False
rec_flag = 1
win = visual.Window(
    size=(1920, 1080),
    fullscr=True,
    units="pix",
    screen=2,
)

trials = 200
default_shader = win._progSignedTexMask

if rec_flag==1:
    ser=serial.Serial("COM5", baudrate=9600)
    #ser2=serial.Serial("COM13", baudrate=9600)
    trials = 20

noise = np.random.uniform(0, 1, (2048, 2048))

noise_tex = visual.GratingStim(
    win=win,
    tex=noise,
    mask=None,
    #size=(1920,1920),
    size = 500000
)

shader = """
(sin((textureFrag.rgb * 2.0 * radians(180.0)) + (((gl_Color.rgb * 2.0) - 1.0) * 2.0 * radians(180.0))) + 1.0) / 2.0;
"""

frag_shader = visual.shaders.fragSignedColorTexMask.replace(
    "gl_FragColor.rgb = (textureFrag.rgb* (gl_Color.rgb*2.0-1.0)+1.0)/2.0;",
    "gl_FragColor.rgb = " + shader
)

shader = visual.shaders.compileProgram(
    vertexSource=visual.shaders.vertSimple,
    fragmentSource=frag_shader
)

phase = 0.0
duration = 0.5

frames_per_cycle = 60
frame_number = int(duration*frames_per_cycle)
tf = 4

phase_inc = tf / frames_per_cycle

noise_tex.color = phase

core.wait(4.0)

for tr in range(trials):
    print tr
    if rec_flag==1:
        ser.write('1')
        #ser2.write('1')
    core.wait(0.5)
    for frame in range(frame_number):

        win._progSignedTexMask = shader

        noise_tex.draw()

        # reset the shader
        win._progSignedTexMask = default_shader

        win.flip()

        #keys = psychopy.event.getKeys()

        #keep_going = ("q" not in keys)

        phase = np.mod(phase + phase_inc, 1)

        noise_tex.color = phase
    win.flip()
    core.wait(10)
win.close()