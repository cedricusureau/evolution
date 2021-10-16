from src import parse_config, debug, toolbox
from src import object
import pygame

VARIABLES = parse_config.parse_config_file("config")
CELL_NUMBER = VARIABLES["cell_number"]

def init():
    pygame.init()

    # initialise l'object "board", que je remplis avec fill. Fill permet de remplir Board.map d'objet "cell".
    board = object.board()
    board.fill()

    # Certaines cellules deviennent vivante :
    board.make_random_cell_alive(CELL_NUMBER)

    # Je dessine le board avec tout les cells dans board.map
    board.draw()
    pygame.display.flip()
    debug.print_first_cell_variable(board)

    return board