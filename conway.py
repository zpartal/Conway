import pygame, sys
from pygame.locals import *

screen_width = 640
screen_height = 480

pygame.init()
DISPLAYSURF = pygame.display.set_mode((screen_width, screen_height),0,32)
pygame.display.set_caption('Conway')
while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()