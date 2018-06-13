# John Conway's game of life
# all code by George A. Merrill (except where otherwise noted)
#################################################################################################
#version 0.0.4 June 13th 2018
#fixed overpopulation check
#improved speed by checking only 8 cells instead of checking every cell is a neighbour
#################################################################################################
#version 0.0.2  June 12th 2018
#added graphics
#################################################################################################
#version 0.0.1  June 12th 2018
#computes all cell states before updating any of them
#################################################################################################
#version 0.0.0
#The Game of Life, also known simply as Life, is a cellular automaton
#  devised by the British mathematician John Horton Conway in 1970
#The universe of the Game of Life
#is an infinite, two-dimensional orthogonal grid of square cells,
# each of which is in one of two possible states, alive or dead,
# Every cell interacts with its eight neighbours,
# which are the cells that are horizontally, vertically, or diagonally adjacent.
# At each step in time, the following transitions occur:
#Any live cell with fewer than two live neighbors dies, as if by under population.
#Any live cell with two or three live neighbors lives on to the next generation.
#Any live cell with more than three live neighbors dies, as if by overpopulation.
#Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
###############################################################################################
from graphics import *#graphics.py by John Zelle
import time
import random as rd
def cellUpdate(cells):
    tempCells = [[0 for x in range(100)] for y in range(100)]
    #first copy old cell states
    for j in range(1,99):
        for i in range(1,99):
            tempCells[i][j] = cells[i][j]

    #calculate  new cell states and store them in tempCells
    for j in range(1,99):
        for i in range(1,99):
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
                tempCells[i][j] = 1
            elif (cells[i][j] == 1 and nbors >= 4) or (cells[i][j] == 1 and nbors < 2):
                tempCells[i][j] = 0
    #last update cells with new states
    for j in range(1,99):
        for i in range(1,99):
            cells[i][j] = tempCells[i][j]
    return
def showGame(cells, win):
    bg = Rectangle(Point(0,0),Point(500,500))
    bg.setFill('white')
    bg.draw(win)
    win.update()
    for j in range(1,99):
        for i in range(1,99):

            if (cells[j][i] == 1):
                dc = Rectangle(Point(i*5,j*5), Point(i*5+4, j*5+4))
                dc.setFill('black')
                dc.draw(win)
    win.update()

def main():
    cells = [[0 for x in range(100)] for y in range(100)]
    for r in range(550):
        x = rd.randint(1,99)
        y = rd.randint(1,99)
        cells[x][y] = 1


    win = GraphWin('game of life', 500, 500, autoflush=False)

    for d in range(200):
        cellUpdate(cells)
        showGame(cells,win)
    #time.sleep(1)
    message = Text(Point(win.getWidth()/2,20), 'Click anywhere to quit.')
    message.draw(win)
    win.getMouse()
    win.close()
main()