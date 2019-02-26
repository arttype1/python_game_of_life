import sys
import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
fonts = {'default': GLUT_BITMAP_TIMES_ROMAN_24, 'gen_count': GLUT_BITMAP_TIMES_ROMAN_24}
colors = {'default': (0,0,0), 'gen_count': (.8, .3, .8)}


def draw_message(style, coord, message):
    r,g,b = colors[style]
    x,y = coord
    glColor3f(r, g, b)
    glRasterPos2d(x, y)
    for c in message:
        glutBitmapCharacter(fonts[style], ord(c))


class Button:
    def __init__(self,color1,color2, x1, y1, x2, y2):
        self.color1 = color1
        self.color2 = color2
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.message = ''
        self.style = 'default'

    def draw(self):
        r,g,b = self.color1
        glColor3f(r, g, b)
        glRecti(self.x1, self.y1, self.x2, self.y2)
        r,g,b = self.color2
        glColor3f(r, g, b)
        glRecti(self.x1 + 2, self.y1 + 2, self.x2 - 2, self.y2 - 2)
        if self.message != '':
            draw_message(self.style, (self.x1 + 5, self.y1 + 5), self.message)

    def is_inside(self,x, y):
        if (self.x1 < x < self.x2) and (self.y1 < y < self.y2):
            return True
        else:
            return False


class Canvas:
    """
    viewport and window are lists (left, right, bottom, top)
    color is used for drawing (red, green, blue)
    """
    def __init__(self, width, height, window_title: str):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(width, height)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(window_title.encode('ascii'))
        self.window = [0, width, 0,  height]
        self.viewport = [0, width, 0,  height]
        self.color = [0, 0, 0]
        self.set_window(0, width, 0, height)
        self.set_viewport(0, width, 0, height)

    @staticmethod
    def swap():
        glutSwapBuffers()

    @staticmethod
    def clear_screen():
        glClear(GL_COLOR_BUFFER_BIT)

    @staticmethod
    def set_bc(r, g, b):
        glClearColor(r, g, b, 0.0)

    @staticmethod
    def thick(t):
        glLineWidth(t)

    def set_color(self, r, g, b):
        self.color = [r, g, b]
        glColor3f(r, g, b)

    def set_window(self, l, r, b, t):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(l, r, b, t)
        self.window = [l , r, b, t]

    def set_viewport(self, left, right, bottom, top):
        glViewport(left, bottom, right - left, top - bottom)
        self.viewport = [left, right, bottom, top]