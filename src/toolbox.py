import random, string
import math
import os
from src import object

def get_some_random_cell(map_size, nb_of_cell_to_get, country, country_len, frontier_size):

    # ##On fait un dictionnaire avec toutes les positions possibles appartenant aux pays (country, qui contient le
    # nom du pays). Dépend de la longueur d'un pays "country_len"

    country_loc = {}
    for name, pos in country.items():
        country_loc[name] = [(x, y) for x in range(pos[0], pos[0]+country_len-frontier_size) for y in range(pos[1], pos[1]+country_len-frontier_size)]

    cell_country_attribution = {}

    for i in range(nb_of_cell_to_get):
        tmp_cell_id = make_random_id(10)
        tmp_country = random.choice(list(country_loc.keys()))
        random_loc = random.choice(country_loc[tmp_country])
        country_loc[tmp_country].remove(random_loc)
        if len(country_loc[tmp_country]) == 0:
            country_loc.pop(tmp_country)

        cell_country_attribution[tmp_cell_id] = [tmp_country, random_loc]


    return cell_country_attribution


def make_random_id(id_size):
    lower = string.ascii_uppercase
    tmp = random.sample(lower, id_size)
    return "".join(tmp)


def make_country(map_size, country_numbers, country_size):
    country_len = round(map_size / country_size)

    country_tl = []
    for i in range(0, map_size-country_len+1, country_len):
        for j in range(0, map_size-country_len+1, country_len):
            country_tl.append((i, j))

    country_location = {}
    for i in range(country_numbers):
        country_ID = make_random_id(5)
        random_loc = random.choice(country_tl)
        country_tl.remove(random_loc)
        country_location[country_ID] = random_loc

    return country_location, country_len

def give_cell_direction(country, country_list, country_len, frontier_size):


    house_pos_x = random.randint(country_list[country][0], country_list[country][0]+country_len-frontier_size)
    house_pos_y = random.randint(country_list[country][1], country_list[country][1]+country_len-frontier_size)

    work_pos_x = random.randint(country_list[country][0], country_list[country][0]+country_len-frontier_size)
    work_pos_y = random.randint(country_list[country][1], country_list[country][1]+country_len-frontier_size)

    hobbie_pos_x = random.randint(country_list[country][0], country_list[country][0]+country_len-frontier_size)
    hobbie_pos_y = random.randint(country_list[country][1], country_list[country][1]+country_len-frontier_size)

    other_country_list = [i for i in country_list.keys() if i != country]

    if len(other_country_list) > 0:
        travel_destination = random.choice(other_country_list)
        travel_destination_x = random.choice(list(range(country_list[travel_destination][0], country_list[travel_destination][0]+country_len-frontier_size)))
        travel_destination_y = random.choice(list(range(country_list[travel_destination][1], country_list[travel_destination][1] + country_len-frontier_size)))

        return (house_pos_x, house_pos_y), (work_pos_x, work_pos_y), (hobbie_pos_x, hobbie_pos_y), (travel_destination_x, travel_destination_y)
    else:
        return (house_pos_x, house_pos_y), (work_pos_x, work_pos_y), (hobbie_pos_x, hobbie_pos_y), (house_pos_x, house_pos_y)

def get_new_position(location, destination):

    speed = random.randint(1,1)

    if location[0] < destination[0]:
        new_x = location[0]+speed
    elif location[0] > destination[0]:
        new_x = location[0]-speed
    elif location[0] == destination[0]:
        new_x = location[0]

    if location[1] < destination[1]:
        new_y = location[1]+speed
    elif location[1] > destination[1]:
        new_y = location[1]-speed
    elif location[1] == destination[1]:
        new_y = location[1]

    return (new_x, new_y)

def calcul_distance_to_destination(p1, p2):
    distance = math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))
    return distance

def make_some_random_disease(n):
    all_disease = {}
    all_images = ["random_image/"+i for i in os.listdir("random_image") if ".png" in i]

    for i in range(n):
        d = object.Disease(all_images[i])
        all_disease[d.id] = d

    return all_disease

def get_some_alive_cell(alive_map, nb_of_cell_to_get):
    cells = random.sample(alive_map, nb_of_cell_to_get)
    return cells

def get_sick_cell_pos(board_map):
    sick_cell_pos = []
    for col in range(len(board_map)):
        for ligne in range(len(board_map)):
            cell = board_map[col][ligne]
            if cell.sick:
                sick_cell_pos.append(cell.location)

    return sick_cell_pos

def get_alive_cell_around(cell_pos, map_size, board):
    arround = [(cell_pos[0] - 1, cell_pos[1]), (cell_pos[0] + 1, cell_pos[1]), (cell_pos[0], cell_pos[1] - 1),
               (cell_pos[0], cell_pos[1] + 1)]

    arround_to_push = []
    for cell in arround:
        x, y = cell[0], cell[1]

        if (x < map_size) & (y < map_size) & (x >= 0) & (y >= 0):
            tmp_cell = board.map[x][y]
            if tmp_cell.alive:
                arround_to_push.append(cell)

    return arround_to_push

def get_whate_image_to_pick(cell_disease):
    """
    Une cellule peut être atteinte de plusieurs maladie. Cette fonction renvoie la maladie dont la létalité est la plus haute
    En effet, pour afficher la cellule de la bonne couleur, on choisi d'affiché la maladie la plus dangereuse.
    """

    top_letalite = 0
    top_image = ""
    if len(cell_disease) == 1:
        return list(cell_disease.values())[0].id

    for id, d in cell_disease.items():
        if not d.immun:
            if d.letalite > top_letalite:
                top_letalite = d.letalite
                top_image = d.id

    return top_image

def get_new_born(country, country_list, country_len, frontier_size, alive_map):

    pos_ok = False
    while pos_ok == False:
        house_pos_x = random.randint(country_list[country][0], country_list[country][0] + country_len - frontier_size)
        house_pos_y = random.randint(country_list[country][1], country_list[country][1] + country_len - frontier_size)
        if (house_pos_x, house_pos_y) not in alive_map:
            pos_ok = True

    return country, (house_pos_x, house_pos_y)