# https://en.wikipedia.org/wiki/Spirograph
# https://python-opengl-examples.blogspot.com/
from multiprocessing.connection import Listener
import pygame, pygame_widgets
#from pygame_widgets.slider import Slider
from OpenGL.GL import *
from ctypes import sizeof, c_void_p

from ast import literal_eval as make_tuple

# Address context error if pygame/pyOpenGL EGL vs. Wayland mismatch:
# https://github.com/pygame/pygame/issues/3110
import os
os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

from graphics import VERTEX_SHADER_SOURCE, FRAGMENT_SHADER_SOURCE, initOpenGL

import time

address =('localhost', 6123)
listener =  Listener(address, authkey=b'secret')
print("Listener at address: ", address)
#conn = listener.accept()
print("Got connection to controller:", listener.last_accepted)

pygame.init()
display = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF|pygame.OPENGL)
pygame.display.set_caption('SpirographGL')
clock = pygame.time.Clock()
FPS = 160

#slider = Slider(display, 100, 100, 800, 40, min=0, max=99, step=1)

vertices = [0.0 if not i%3==2 else float(i//4+1) for i in range(0,120000)]
print(vertices[0:100])

vertices = (GLfloat * len(vertices))(*vertices)  
program, vao = initOpenGL(vertices)

conn = listener.accept()
m=0.8
msg=""
while True:
    time.sleep(0.01)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    #glClearColor(1.0, 0.6, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(program)
    myUniformLocation1 = glGetUniformLocation(program, r"param_radiusRatio")
    myUniformLocation2 = glGetUniformLocation(program, r"param_holePosition")

    #o=int(conn.recv())
    while conn.poll():
         msg = conn.recv()
    try:     
        print("SLAVE: ", msg)
        o=float(make_tuple(msg)[1])
    except ValueError:
        o=0.11111
    except SyntaxError:
        o=0.22222

    glUniform1f(myUniformLocation1, o);
    glUniform1f(myUniformLocation2, m);
    
    
    print(o)

    glBindVertexArray(vao)
    glDrawArrays(GL_LINE_STRIP, 0, 120000)

    pygame_widgets.update(event)
    pygame.display.flip()
    #pygame.display.update()
    clock.tick(FPS)
    
listener.close()
