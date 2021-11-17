from src import parse_config, debug, toolbox, images
from src import object
import pygame

VARIABLES = parse_config.parse_config_file("config")
CELL_NUMBER = VARIABLES["cell_number"]
SICK_CELL_NUMBER = VARIABLES["sick_cell_number"]

def init():

    images.make_some_image(VARIABLES["disease_generated"])
    all_disease = toolbox.make_some_random_disease(VARIABLES["disease_generated"])

    pygame.init()

    # initialise l'object "board", que je remplis avec fill. Fill permet de remplir Board.map d'objet "cell".
    board = object.board(all_disease)
    board.fill()

    # Certaines cellules deviennent vivante :
    board.make_random_cell_alive(CELL_NUMBER)
    board.make_random_cell_sick(SICK_CELL_NUMBER)
    # Je dessine le board avec tout les cells dans board.map
    board.draw()
    pygame.display.flip()
    debug.print_first_cell_variable(board)

    return board