"""
John Conway's game of life
all code by George A. Merrill

The Game of Life, also known simply as Life, is a cellular automaton
  devised by the British mathematician John Horton Conway in 1970
The universe of the Game of Life
is an infinite, two-dimensional orthogonal grid of square cells,
each of which is in one of two possible states, alive or dead,
Every cell interacts with its eight neighbours,
which are the cells that are horizontally, vertically, or diagonally adjacent.
At each step in time, the following transitions occur:
Any live cell with fewer than two live neighbors dies, as if by under population.
Any live cell with two or three live neighbors lives on to the next generation.
Any live cell with more than three live neighbors dies, as if by overpopulation.
Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
###############################################################################################
version 0.0.01 start of OpenGl
version 0.0.02 cell updates and display
version 0.0.03 start of menu
"""
from Canvas import Canvas
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time
from random import randint
screen_width = 1885
screen_height = 1025
cvs = Canvas(screen_width, screen_height, 'Game of Life')
cells = [[0 for x in range(200)] for y in range(200)]
count = 0

def draw_message(color, coord, message):
    r,g,b = color
    x,y = coord
    glColor3f(r, g, b)
    glRasterPos2d(x, y)
    for c in message:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))


def cell_update():
    global cells
    temp_cells = [[0 for x in range(200)] for y in range(200)]
    # first copy old cell states
    for j in range(1,199):
        for i in range(1,199):
            temp_cells[i][j] = cells[i][j]

    # calculate  new cell states and store them in temp_cells
    for j in range(1,199):
        for i in range(1,199):
            nbors = 0
            if cells[i][j-1] == 1:
                nbors += 1
            if cells[i][j+1] == 1:
                nbors += 1
            if cells[i-1][j-1] == 1:
                nbors += 1
            if cells[i-1][j] == 1:
                nbors += 1
            if cells[i-1][j+1] == 1:
                nbors += 1
            if cells[i+1][j-1] == 1:
                nbors += 1
            if cells[i+1][j] == 1:
                nbors += 1
            if cells[i+1][j+1] == 1:
                nbors += 1
            if cells[i][j] == 0 and nbors == 3:
                temp_cells[i][j] = 1
            elif cells[i][j] == 1 and nbors >= 4 or nbors < 2:
                temp_cells[i][j] = 0
    # last update cells with new states
    for j in range(1,199):
        for i in range(1,199):
            cells[i][j] = temp_cells[i][j]
    glutPostRedisplay()


def draw_menu_bar():
    glColor3f(.9, .9, .9)
    glRecti(0, screen_height - 19, screen_width, screen_height)
    glColor3f(0, 0, 0)
    glRasterPos2d(2, screen_height - 15)
    for c in 'File':
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(c))
    glRecti(2, screen_height - 16, 11, screen_height - 17)


def my_pass(x, y):
    y = screen_height -y
    glutPostRedisplay()


def my_display():
    global cvs, cells, count
    global red_dot
    glutUseLayer(GLUT_NORMAL)
    cvs.set_bc(0, 0, 0)
    cvs.clear_screen()
    glPointSize(4)
    glColor3f(1, 1, 1)
    glRecti(0,0,800,800)
    glColor3f(.6, .6, 1)
    glRecti(2,2,798,798)
    glColor3f(0, 0, 0)
    glBegin(GL_POINTS)
    for j in range(1,199):
        for i in range(1,199):
            if cells[j][i] == 1:
                glVertex2i(j*4, i*4)
    glEnd()
    draw_message((.8, .3, .8),  (500, 900),f'current GENERATION: {count}')
    draw_menu_bar()
    cvs.swap()
    count += 1
    if count > 2000:
        quit()
    cell_update()



x=100
y=100
for r in range(500):
    dx = randint(0,1)
    dy = randint(0,1)
    x,y = x + dx * 2 - 1, y + dy * 2 - 1
    cells[x][y] = 1

glutDisplayFunc(my_display)
glutPassiveMotionFunc(my_pass)
glutMainLoop()

