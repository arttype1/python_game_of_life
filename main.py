# John Conway's game of life
# all code by George A. Merrill (except where otherwise noted)
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
def cellUpdate(cells):
    tempCells = [[0 for x in range(10)] for y in range(10)]
    #first copy old cell states
    for j in range(10):
        for i in range(10):
            tempCells[i][j] = cells[i][j]

    #calculate  new cell states and store them in tempCells
    for j in range(10):
        for i in range(10):
            nbors = 0
            for x in range(10):
                for y in range(10):
                    distN = (abs(i - x) + abs(j - y))
                    if (distN == 1) or (distN == 2 and x != i and y != j):
                        if cells[x][y] == 1:
                            nbors += 1
            if cells[i][j] == 0 and nbors == 3:
                tempCells[i][j] = 1
            elif (cells[i][j] == 1 and nbors > 4) or (cells[i][j] == 1 and nbors < 2):
                tempCells[i][j] = 0
    #last update cells with new states
    for j in range(10):
        for i in range(10):
            cells[i][j] = tempCells[i][j]
    return
def main():
    cells = [[0 for x in range(10)] for y in range(10)]
    cells[3][3] = 1
    cells[3][4] = 1
    cells[3][5] = 1
    cells[0][2] = 0


    for d in range(3):
        print(repr(d) + '--------------------------')
        for c in range(10):
            print ('[' + repr(cells[c][0])+'], ['+ repr(cells[c][1])+'], ['+ repr(cells[c][2])+'], ['+ repr(cells[c][3])+'], ['+ repr(cells[c][4])+'], ['+ repr(cells[c][5])+'], ['+ repr(cells[c][6])+'], ['+ repr(cells[c][7])+'], ['+ repr(cells[c][8])+'], ['+ repr(cells[c][9])+']')
        cellUpdate(cells)
main()