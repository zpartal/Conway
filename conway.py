# Conway Game of Life
# Zachary Partal

import pygame, random, sys, math
from pygame.locals import *

cell_size = 10 # size of cells in pixels
grid_width = 64
grid_height = 48
window_width = grid_width * cell_size
window_height = grid_height * cell_size
FPS = 30

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
BGCOLOR = WHITE


class cell:
    def __init__(self, x, y):
        self.pos_x = x # horizontal cell grid position
        self.pos_y = y # vertical cell grid position
        self.state = 0 # 1 for alive, 0 for dead
    def print_loc(self):
        print(str(self.pos_x) + "," + str(self.pos_y))
    def kill(self):
        self.state = 0
    def live(self):
        self.state = 1

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, cell_table
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((window_width, window_height),0,32)
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Conway')
    cell_table = generateCells()
    runGame()

def runGame():
    running_state = 0 # 0 if game is not running, 1 if game is running
    mouse_x = 0
    mouse_y = 0    

    while True: # main game loop
        mouseClicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouseClicked = True
                if running_state == 0:
                    activate_cell(mouse_x,mouse_y)
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if running_state == 0:
                        running_state = 1
                        startSim()
                    else: running_state = 0
                elif event.key == K_c:
                    if running_state == 0:
                        reset_cells()

        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawCells(cell_table)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generateCells():
    cell_table = []
    for x in range(grid_width):
        new_column = []
        for y in range(grid_height):
            new_column.append(cell(x,y))
        cell_table.append(new_column)
    return cell_table

def startSim():
    pass

def activate_cell(_mouse_x, _mouse_y):
    gridx = math.floor( _mouse_x / cell_size )
    gridy = math.floor( _mouse_y / cell_size )
    # print("[" + str(_mouse_x) + "," + str(_mouse_y) + "], [" + str(gridx) + "," + str(gridy) + "]")
    if cell_table[gridx][gridy].state == 1:
        cell_table[gridx][gridy].kill()
    else:
        cell_table[gridx][gridy].live()

def reset_cells():
    for x in range(grid_width):
        for y in range(grid_height):
            cell_table[x][y].kill()

def drawGrid():
    for x in range(0, window_width, cell_size): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, BLACK, (x, 0), (x, window_height))
    for y in range(0, window_height, cell_size): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, BLACK, (0, y), (window_width, y))

def drawCells(_cell_table):
    for x in range(grid_width):
        for y in range(grid_height):
            if _cell_table[x][y].state == 1:
                rect_coords = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
                pygame.draw.rect(DISPLAYSURF, BLACK, rect_coords)

if __name__ == '__main__':
    main()