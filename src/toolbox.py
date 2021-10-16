import random, string


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

def give