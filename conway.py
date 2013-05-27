# Conway Game of Life
# Zachary Partal

import pygame, random, sys, math
from pygame.locals import *

CELLSIZE = 10 # size of cells in pixels
GRIDWIDTH = 5
GRIDHEIGHT = 5
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

class Cell:
    pos_x = 0 # horizontal cell grid position
    pos_y = 0 # vertical cell grid position
    state = 0 # 1 for alive, 0 for dead
    def __init__(self, x, y):
        self.pos_x = x # horizontal cell grid position
        self.pos_y = y # vertical cell grid position
    def print_loc(self):
        print(str(pos_x) + "," + str(pos_y))
    def kill(self):
        self.state = 0
    def live(self):
        self.state = 1
    def isAlive(self):
        if self.state == 1:
            return True
        else: 
            return False

class CellBoard:
    cell_table = []
    next_state = []
    width = 0
    height = 0
    def __init__(self, _width, _height):
        self.width = _width
        self.height = _height
        for x in range(self.width):
            new_column = []
            for y in range(self.height):
                new_column.append(Cell(x,y))
            self.cell_table.append(new_column)
            self.next_state.append(new_column)

    def clear_board(self):
        for x in range(self.width):
            for y in range(self.height):
                self.cell_table[x][y].kill()

    def num_neighbors(self, _x, _y):
        neighbor_count = 0
        for x in range(-1,2):
            for y in range(-1,2):
                # print("[" + str(_x+x) + "," + str(_y+y) + "]")
                if x == 0 and y == 0: pass
                elif _x+x >= self.width or _y+y >= self.height: pass
                elif _x+x < 0 or _y+y < 0: pass
                else:
                    # print("[" + str(_x+x) + "," + str(_y+y) + "]")
                    if self.cell_table[_x+x][_y+y].isAlive():                    
                        neighbor_count += 1
        # print("neighbor count: " + str(neighbor_count))
        return neighbor_count

    def update_cell_state(self, _x, _y):
        live_neighbors = num_neighbors(_x, _y)
        # print("Cell: [" + str(_x) + "," + str(_y) + "] Neighbors: " + str(live_neighbors))
        if live_neighbors < 2: self.next_state[_x][_y].kill()
        elif live_neighbors >= 2 and live_neighbors <= 3: self.next_state[_x][_y].live()
        elif live_neighbors > 3: self.next_state[_x][_y].kill()

    def generate_next_state(self):
        for x in range(self.width):
            for y in range(self.height):
                update_cell_state(x, y)
        self.cell_table = self.next_state

    def cell(self, _x, _y):
        return self.cell_table[_x][_y]

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, game_board, running_state
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((window_width, window_height),0,32)
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Conway')
    game_board = CellBoard(GRIDWIDTH, GRIDHEIGHT)
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
                        game_board.clear_board()

        DISPLAYSURF.fill(BGCOLOR)
        if running_state == 1:
            pass
            # game_board.generate_next_state()
        drawGrid()
        drawCells()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def click_cell(_mouse_x, _mouse_y):
    gridx = math.floor( _mouse_x / CELLSIZE )
    gridy = math.floor( _mouse_y / CELLSIZE )
    if game_board.cell(gridx,gridy).isAlive():
        game_board.cell(gridx,gridy).kill()
    else:
        game_board.cell(gridx,gridy).live()
    print("Clicked: [" + str(gridx) + "," + str(gridy) + "], state: " + str(game_board.cell_table[gridx][gridy].state))

def print_neighbor_count(_mouse_x, _mouse_y):
    gridx = math.floor( _mouse_x / CELLSIZE )
    gridy = math.floor( _mouse_y / CELLSIZE )
    print(str(game_board.num_neighbors(gridx,gridy)))

def drawGrid():
    for x in range(0, window_width, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, BLACK, (x, 0), (x, window_height))
    for y in range(0, window_height, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, BLACK, (0, y), (window_width, y))

def drawCells():
    for x in range(GRIDWIDTH):
        for y in range(GRIDHEIGHT):
            if game_board.cell(x,y).isAlive():
                rect_coords = pygame.Rect(x*CELLSIZE, y*CELLSIZE, CELLSIZE, CELLSIZE)
                pygame.draw.rect(DISPLAYSURF, BLACK, rect_coords)

if __name__ == '__main__':
    main()