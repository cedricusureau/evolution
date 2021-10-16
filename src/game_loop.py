from src import initialize
from src.object import *
import pygame
from pygame.locals import *

def game():
    board = initialize.init()

    done=False
    while done == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True


        # board.make_one_moove()
        # board.draw()
        # pygame.display.flip()