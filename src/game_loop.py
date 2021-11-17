from src import initialize
from src.object import *
import pygame, time
from pygame.locals import *

VARIABLES = parse_config.parse_config_file("config")

def game():
    board = initialize.init()
    count = 0
    done=False
    while done == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True

        board.make_one_moove()
        board.incubate()
        board.contaminate()
        board.make_some_friend()

        pygame.display.flip()
        board.draw()

        count += 1
        if count % 50 == 0:
            board.make_random_cell_sick(1)
            print(count)

        time.sleep(VARIABLES["time_sleep"])