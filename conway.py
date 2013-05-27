# Conway Game of Life
# Zachary Partal

import pygame, random, sys, math
from pygame.locals import *

CELLSIZE = 10 # size of cells in pixels
GRIDWIDTH = 64
GRIDHEIGHT = 48
window_width = GRIDWIDTH * CELLSIZE
window_height = GRIDHEIGHT * CELLSIZE
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
    global FPSCLOCK, DISPLAYSURF, BASICFONT, cell_table, running_state
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((window_width, window_height),0,32)
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Conway')
    cell_table = generateCells()
    running_state = 0 # 0 if game is not running, 1 if game is running
    runGame()

def runGame():    
    mouse_x = 0
    mouse_y = 0
    running_state = 0
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
                    click_cell(mouse_x,mouse_y)
                elif running_state == 1:
                    print_neighbor_count(mouse_x,mouse_y)
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if running_state == 0:
                        running_state = 1
                        print("Game Running")
                    else: 
                        running_state = 0
                        print("Not Running")
                elif event.key == K_c:
                    if running_state == 0:
                        reset_cells()

        DISPLAYSURF.fill(BGCOLOR)
        if running_state == 1:
            generateCells()
        drawGrid()
        drawCells(cell_table)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generateCells():
    cell_table = []
    for x in range(GRIDWIDTH):
        new_column = []
        for y in range(GRIDHEIGHT):
            new_column.append(cell(x,y))
        cell_table.append(new_column)
    return cell_table

def generate_state():
    # Any live cell with fewer than two live neighbors dies, as if caused by under-population.
    # Any live cell with two or three live neighbors lives on to the next generation.
    # Any live cell with more than three live neighbors dies, as if by overcrowding.
    # Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
    new_state = cell_table
    for x in range(GRIDWIDTH):
        for y in range(GRIDHEIGHT):
            update_cell_state(new_state, cell_table, x, y)
    cell_table = new_state

def num_neighbors(current_state, _x, _y):
    neighbor_count = 0
    for x in range(-1,2):
        for y in range(-1,2):
            # print("[" + str(_x+x) + "," + str(_y+y) + "]")
            if x == 0 and y == 0: pass
            elif _x+x >= GRIDWIDTH or _y+y >= GRIDHEIGHT: pass
            elif _x+x < 0 or _y+y < 0: pass
            else:
                # print("[" + str(_x+x) + "," + str(_y+y) + "]")
                if cell_table[_x+x][_y+y].state == 1:                    
                    neighbor_count += 1
    # print("neighbor count: " + str(neighbor_count))
    return neighbor_count

def update_cell_state (new_state, current_state, _x, _y):
    live_neighbors = num_neighbors(current_state, _x, _y)
    if live_neighbors < 2: new_state[_x][_y].kill()
    elif live_neighbors >= 2 and live_neighbors <= 3: new_state[_x][_y].live()
    elif live_neighbors > 3: new_state[_x][_y].kill()

def click_cell(_mouse_x, _mouse_y):
    gridx = math.floor( _mouse_x / CELLSIZE )
    gridy = math.floor( _mouse_y / CELLSIZE )
    print("Clicked: [" + str(gridx) + "," + str(gridy) + "]")
    # print("Clicked: [" + str(_mouse_x) + "," + str(_mouse_y) + "], [" + str(gridx) + "," + str(gridy) + "]")
    if cell_table[gridx][gridy].state == 1:
        cell_table[gridx][gridy].kill()
    else:
        cell_table[gridx][gridy].live()

def print_neighbor_count(_mouse_x, _mouse_y):
    gridx = math.floor( _mouse_x / CELLSIZE )
    gridy = math.floor( _mouse_y / CELLSIZE )
    print(str(num_neighbors(cell_table, gridx,gridy)))

def reset_cells():
    for x in range(GRIDWIDTH):
        for y in range(GRIDHEIGHT):
            cell_table[x][y].kill()

def drawGrid():
    for x in range(0, window_width, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, BLACK, (x, 0), (x, window_height))
    for y in range(0, window_height, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, BLACK, (0, y), (window_width, y))

def drawCells(_cell_table):
    for x in range(GRIDWIDTH):
        for y in range(GRIDHEIGHT):
            if _cell_table[x][y].state == 1:
                rect_coords = pygame.Rect(x*CELLSIZE, y*CELLSIZE, CELLSIZE, CELLSIZE)
                pygame.draw.rect(DISPLAYSURF, BLACK, rect_coords)

if __name__ == '__main__':
    main()