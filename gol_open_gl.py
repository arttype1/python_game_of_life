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
version 0.0.04 start of gui
version 0.0.05 boarder wrapping
"""
from Cangui import *
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
game_mode = 'pause'
wrap = True
button_pause = Button((0.5, 0.5, 0.5), (0.7, 0.7, 0.7), 900, 500, 990, 530)
button_pause.message = 'START'


def cell_update_wrap():
    global cells, game_mode, count
    if game_mode == 'play':
        count += 1
        temp_cells = [[0 for x in range(200)] for y in range(200)]
        # first copy old cell states
        for j in range(0, 200):
            for i in range(0, 200):
                temp_cells[i][j] = cells[i][j]
        # calculate  new cell states and store them in temp_cells
        for j in range(0, 200):
            for i in range(0, 200):
                nbors = 0
                if (j>0 and cells[i][j-1] == 1) or (j==0 and cells[i][199] == 1):
                    nbors += 1
                if(j<199 and cells[i][j+1] == 1) or (j==199 and cells[i][0] == 1):
                    nbors += 1
                if(i>0 and j>0 and cells[i-1][j-1] == 1) or (i==0 and j==0 and cells[199][199] == 1)\
                        or (i>0 and j==0 and cells[i-1][199] == 1) or (i==0 and j>0 and cells[199][j-1] == 1):
                    nbors += 1
                if(i>0 and cells[i-1][j] == 1) or (i==0 and cells[199][j] == 1):
                    nbors += 1
                if(i>0 and j<199 and cells[i-1][j+1] == 1) or (i==0 and j==199 and cells[199][0] == 1)\
                        or (i>0 and j==199 and cells[i-1][0] == 1) or (i==0 and j<199 and cells[199][j+1] == 1):
                    nbors += 1
                if(i<199 and j>0 and cells[i+1][j-1] == 1) or (i==199 and j==0 and cells[0][199] == 1)\
                        or (i<199 and j==0 and cells[i+1][199] == 1) or (i==199 and j>0 and cells[0][j-1] == 1):
                    nbors += 1
                if(i<199 and cells[i+1][j] == 1) or (i==199 and cells[0][j] == 1):
                    nbors += 1
                if(i<199 and j<199 and cells[i+1][j+1] == 1) or (i==199 and j==199 and cells[0][0] == 1)\
                        or (i<199 and j==199 and cells[i+1][0] == 1) or (i==199 and j<199 and cells[0][j+1] == 1):
                    nbors += 1
                if cells[i][j] == 0 and nbors == 3:
                    temp_cells[i][j] = 1
                elif cells[i][j] == 1 and nbors >= 4 or nbors < 2:
                    temp_cells[i][j] = 0
        # last update cells with new states
        for j in range(0,200):
            for i in range(0,200):
                cells[i][j] = temp_cells[i][j]
    glutPostRedisplay()


def cell_update():
    global cells, game_mode, count, wrap
    if game_mode == 'play':
        count += 1
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


def my_mouse(button, state, x, neg_y):
    y = screen_height - neg_y
    global game_mode
    if game_mode == 'start':
        pass
    elif game_mode == 'play':
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and \
                button_pause.is_inside(x, y):
            game_mode = 'pause'
    elif game_mode == 'pause':
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and \
                button_pause.is_inside(x, y):
            game_mode = 'play'


def my_display():
    global cvs, cells, count, wrap
    global game_mode
    global button_pause
    if game_mode == 'pause':
        button_pause.message = ' PLAY'
    elif game_mode == 'play':
        button_pause.message = 'PAUSE'
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
    draw_message('gen_count',  (500, 900), f'current GENERATION: {count}')
    button_pause.draw()
    draw_menu_bar()
    cvs.swap()
    if wrap:
        cell_update_wrap()
    else:
        cell_update()



x=100
y=100
for r in range(420):
    dx = randint(0,1)
    dy = randint(0,1)
    t = randint(0,1)
    x,y = x + t * (dx * 2 - 1), y + (1- t) * (dy * 2 - 1)
    cells[x][y] = (1 - cells[x][y])

glutDisplayFunc(my_display)
glutMouseFunc(my_mouse)
glutMainLoop()

