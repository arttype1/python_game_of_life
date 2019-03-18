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
version 0.0.01 moving forward with wx instead of GLUT to run the animation
version 0.0.02 added start/play button, population count
version 0.0.03 added generation count
"""
import wx
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
# ----------------------------------------------------------------------
cells = [[0 for x in range(200)] for y in range(200)]
game_mode = 'pause'
pop = 0
count = 0


class GLC(glcanvas.GLCanvas):
    def __init__(self, parent, pos=(0,0), size=(0,0)):
        glcanvas.GLCanvas.__init__(self, parent, -1, attribList=[wx.glcanvas.WX_GL_DOUBLEBUFFER, wx.glcanvas.WX_GL_RGBA], pos=pos, size=size)
        self.Bind(wx.EVT_PAINT, self.on_draw)
        self.Bind(wx.EVT_IDLE, self.cell_update)
        self.context = glcanvas.GLContext(self)
        self.my_clear = (1, 1, 1.0, 0.0)

    def cell_update(self,event):
        if game_mode == 'PLAY':
            global cells, count
            temp_cells = [[0 for x in range(200)] for y in range(200)]
            # first copy old cell states
            for j in range(1, 199):
                for i in range(1, 199):
                    temp_cells[i][j] = cells[i][j]
            # calculate  new cell states and store them in temp_cells
            for j in range(1, 199):
                for i in range(1, 199):
                    nbors = 0
                    if cells[i][j - 1] == 1:
                        nbors += 1
                    if cells[i][j + 1] == 1:
                        nbors += 1
                    if cells[i - 1][j - 1] == 1:
                        nbors += 1
                    if cells[i - 1][j] == 1:
                        nbors += 1
                    if cells[i - 1][j + 1] == 1:
                        nbors += 1
                    if cells[i + 1][j - 1] == 1:
                        nbors += 1
                    if cells[i + 1][j] == 1:
                        nbors += 1
                    if cells[i + 1][j + 1] == 1:
                        nbors += 1
                    if cells[i][j] == 0 and nbors == 3:
                        temp_cells[i][j] = 1
                    elif cells[i][j] == 1 and nbors >= 4 or nbors < 2:
                        temp_cells[i][j] = 0
            # last update cells with new states
            for j in range(1, 199):
                for i in range(1, 199):
                    cells[i][j] = temp_cells[i][j]
            count += 1
        self.on_draw(None)

    def on_draw(self,event):
        """----Main Loop for OpenGL Graphics---------------------------------"""
        global cells, pop, count
        self.SetCurrent(self.context)
        r,b,g,a = self.my_clear
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 800)
        glViewport(0, 0, 800, 800)
        glColor3f(0, 0, 0)
        glPointSize(4)
        glBegin(GL_POINTS)
        for j in range(1, 199):
            for i in range(1, 199):
                if cells[j][i] == 1:
                    glVertex2i(j * 4, i * 4)
        glEnd()
        pop = np.sum(cells)
        self.SwapBuffers()


class TwoPaneApp(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)
        self.filename = ''
        self.dirname = ''
        frame = wx.Frame(None, -1, "RunDemo: ", pos=(0, 0), size = (1660, 830),
                         style=wx.DEFAULT_FRAME_STYLE, name="run a sample")
        self.frame = frame
        self.init_gui()
        win = wx.Panel(frame)
        win.SetSize(800, 400)
        win.SetPosition((10, 10))
        win.Bind(wx.EVT_IDLE, self.on_idle)
        win.SetBackgroundColour('gray')
        sizer = wx.BoxSizer(wx.VERTICAL)
        btn = wx.Button(win, wx.ID_ANY, 'PLAY')
        sizer.Add(btn)
        btn.Bind(wx.EVT_BUTTON, self.on_button)
        btn2 = wx.Button(win, wx.ID_ANY, 'PAUSE')
        sizer.Add(btn2)
        btn2.Bind(wx.EVT_BUTTON, self.on_button)
        win.SetSizer(sizer)
        self.pop_txt = wx.StaticText(win, label=f'Population: {pop}', pos=(100, 100))
        font = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        self.pop_txt.SetFont(font)
        self.count_txt = wx.StaticText(win, label=f'Generation: {count}', pos=(100, 125))
        self.count_txt.SetFont(font)
        self.pop_txt.SetForegroundColour('green')
        self.count_txt.SetForegroundColour('yellow')
        win.Layout()
        win2 = GLC(frame, pos=(825, 10), size=(800, 800))
        self.window1 = win
        self.window2 = win2
        frame.SetBackgroundColour('black')
        frame.SetSize((1650, 880))
        frame.Show(True)
        self.SetTopWindow(frame)

    def init_gui(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        file_item_open = file_menu.Append(wx.ID_OPEN, 'Open', 'Open file')
        file_item_quit = file_menu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menu_bar.Append(file_menu, '&File')
        self.frame.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.on_open, file_item_open)
        self.Bind(wx.EVT_MENU, self.on_quit, file_item_quit)

    def on_open(self, event):
        dlg = wx.FileDialog(self.frame, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            print(f'file name: {self.filename}')
        dlg.Destroy()

    def on_quit(self, event):
        self.frame.Close()

    def on_idle(self, event):
        self.pop_txt.SetLabel(f'Population: {pop}')
        self.count_txt.SetLabel(f'Generation: {count}')

    def on_button(self,event):
        global game_mode
        game_mode = event.GetEventObject().GetLabel()
        self.window2.on_draw(None)


app = TwoPaneApp()


def main():
    x = 100
    y = 100
    global cells
    for r in range(420):
        dx = np.random.randint(0, 2)
        dy = np.random.randint(0, 2)
        t = np.random.randint(0, 2)
        x, y = x + t * (dx * 2 - 1), y + (1 - t) * (dy * 2 - 1)
        cells[x][y] = (1 - cells[x][y])

    app.MainLoop()


main()

