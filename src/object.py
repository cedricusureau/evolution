from src import parse_config, toolbox
import pygame, random

#Toutes les variables permettant de construire les objets :
variables = parse_config.parse_config_file("config")
imgs = ["res/recovered_8.png", "res/dead_8.png"]
map_size = variables["map_size"]
screen_size = variables["screen_size"]

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
alive = pygame.image.load(imgs[0]).convert()
dead = pygame.image.load(imgs[1]).convert()
imgs_size = variables["img_size"]
country_size = variables["country_size"]
frontier_size = variables["frontier_size"]

class cell:
    def __init__(self, location, alive=False):
        self.alive = alive
        self.location = location
        self.sick = False
        self.disease = {}
        self.friends = {}

    def reset(self):
        self.__init__(self.location)

    def make_sick(self, disease):
        self.disease[disease.id] = disease

    #Permet de récupérer tout les attributs d'une cellules dans un dictionnaire, sauf la location
    def __getcellstate__(self):
        d = self.__dict__
        self_dict = {k : d[k] for k in d}
        return self_dict

    #Permet de donné à une cellule tout les attributs extrait de la fonction ci-dessus,
    # et de rajouter la nouvelle location passé en argument
    def __setstate__(self, state, new_loc):
        self.__dict__ = state
        self.__dict__["location"] = new_loc

class board:
    def __init__(self):
        self.map = []
        self.alive_map = []
        self.sick_map = []
        self.dead_cell = []
        self.country, self.country_len = toolbox.make_country(map_size, variables["country_number"], country_size)
    # Je créer un board vide : une liste de liste de cellules vivante ou morte.
    def fill(self):
        for i in range(map_size):
            self.map.append([])
            for g in range(map_size):
                self.map[i].insert(g, cell((i, g)))

    # screen.blit permet d'afficher les bonnes images
    def draw(self):
        for i in range(map_size):
            for g in range(map_size):
                cell = self.map[i][g]
                loc = cell.location

                if cell.alive == True:
                    if cell.sick:
                        #On cherche parmis les maladies de la cellule laquelle afficher
                        # id = get_whate_image_to_pick(cell.disease)
                        try:
                            screen.blit(self.loaded_image[id], (loc[0] * imgs_size, loc[1] * imgs_size))
                        except Exception as e:
                            print(e)
                            print("Problem to blit: ", cell)
                    else:
                        screen.blit(alive, (loc[0] * imgs_size, loc[1] * imgs_size))
                else:
                    screen.blit(dead, (loc[0] * imgs_size, loc[1] * imgs_size))

    # Je tire au sort X cellules que je rends vivante
    def make_random_cell_alive(self, number_of_cells_to_make_alive):
        to_make_alive = toolbox.get_some_random_cell(map_size, number_of_cells_to_make_alive, self.country, self.country_len, frontier_size)
        for cellule_id, information in to_make_alive.items():
            tmp_country=information[0]
            loc = information[1]
            tmp_cell = self.map[loc[0]][loc[1]]
            self.alive_map.append(loc)
            tmp_cell.alive = True
            tmp_cell.name = cellule_id
            tmp_cell.country = tmp_country

            tmp_cell.home, tmp_cell.work,tmp_cell.hobbies, tmp_cell.travel = toolbox.give_cell_direction(tmp_country, self.country_len)

    # Je tire au sort X cellules que je rends malade
    def make_random_cell_sick(self, number_of_cells_to_make_alive):
        to_make_alive = get_some_alive_cell(self.alive_map, number_of_cells_to_make_alive)
        disease_on_board = set()

        for cellule in to_make_alive:
            tmp_cell = self.map[cellule[0]][cellule[1]]
            tmp_disease = random.choice(list(self.all_disease.values()))
            tmp_cell.make_sick(tmp_disease)
            tmp_cell.sick = True
            self.sick_map.append(cellule)
            disease_on_board.add(tmp_disease)

        #On ajoute un nouvel attribut à board : l'ensemble des maladies présentes sur le board.
        self.disease_on_board = disease_on_board

        #On fait également un dictionnaire qui charges les images correspondantes

        loaded_image = {}
        for disease in disease_on_board:
            loaded_image[disease.id] = pygame.image.load(disease.image).convert()

        #Le dictionnaire loaded_image contient les images initialisé Pygame
        self.loaded_image = loaded_image

    def make_one_moove(self):
        to_move = self.alive_map
        # Je boucle sur chaque cellules vivantes

        for indice, old_pos in enumerate(to_move):
            to_replace = True

            while to_replace:
                # Je tire au hasard si je bouge en x en y, vers l'arrière ou vers l'avant
                plus_or_minus = random.choice([-1, +1])
                x_or_y = random.choice(["x", "y"])

                # Je définie la nouvelle positions
                if x_or_y == "x":
                    new_pos = (old_pos[0] + plus_or_minus, old_pos[1])
                else:
                    new_pos = (old_pos[0], old_pos[1] + plus_or_minus)

                # Je vérifie que la nouvelle position soit possible = pas en dehors de la carte, et pas sur sur une
                # cellule vivante
                if (new_pos[0] >= 0) & (new_pos[1] >= 0) \
                        & (new_pos[1] < map_size) \
                        & (new_pos[0] < map_size) \
                        & (new_pos not in self.alive_map):

                    # Je récupère la cellules ancienne position et nouvelle position
                    tmp_cell1 = self.map[old_pos[0]][old_pos[1]]
                    tmp_cell2 = self.map[new_pos[0]][new_pos[1]]

                    #Je transmets toutes les attributs de l'ancienne cellule à la nouvelle, sauf la "location".
                    #La nouvelle position est donné en argument
                    state = tmp_cell1.__getcellstate__()
                    tmp_cell2.__setstate__(state, new_pos)

                    #Je reset la cellule origine = cellule vide
                    tmp_cell1.reset()

                    #Je mets à jour la carte des cellules vivantes.
                    self.alive_map.remove(old_pos)
                    self.alive_map.append(new_pos)

                    # Je sors du while)
                    to_replace = False
                else:
                    break
    def make_some_friend(self):

        for alive_cell in self.alive_map:

            tmp_cell1 = self.map[alive_cell[0]][alive_cell[1]]
            cells_arround = get_alive_cell_around(alive_cell, map_size, self)


    def contaminate(self):
        #On récupère les positions des cellules malades
        sick_cell_pos = get_sick_cell_pos(self.map)

        #On commence a boucler sur toutes positions des cellules malades
        for pos_cell_sick in sick_cell_pos:
            #On récupère l'object contamineur et les cellules environnantes
            contamineur = self.map[pos_cell_sick[0]][pos_cell_sick[1]]
            cells_arround = get_alive_cell_around(pos_cell_sick, map_size, self)

            # Pour chaque cellules environnante, on essaie de voir si elles sont vivantes.
            for cell_pos in cells_arround:
                tmp_cell = self.map[cell_pos[0]][cell_pos[1]]
                if tmp_cell.alive == True:
                    #Si elle est vivante, elle devient malade et
                    #on transmets toutes les maladies de la cellules contaminante

                    #On boucle sur toutes les maladies du contamineur
                    for id, d in contamineur.disease.items():

                        #On vérifie que la cellule n'est pas déjà atteinte par cette maladie
                        #Sinon, on lui transmets l'objet maladie dans son dico
                        #Attention, on reset le temps d'incubation à 0
                        if id not in tmp_cell.disease.keys():

                            #On lance le dé "Contagiosité"
                            dice = random.random()
                            if dice < d.contagiosité :

                                #On récupère les info du contamineur
                                new_disease_carac = d.__getdiseasestate__()

                                #On créer un nouvel object maladie
                                tmp_cell.disease[d.id] =  Disease(d.image)

                                #On lui applique les caractéristiques de l'ancienne maladie
                                tmp_cell.disease[d.id].__setstate__(new_disease_carac)

                                #On remet à 0 le temps malade
                                tmp_cell.disease[d.id].temps_malade = 0

                                #On refixe les état "sick"
                                tmp_cell.sick = True


    def incubate(self):

        #A optimisé, bouclé uniquement sur les cellules malades et pas seulement les cellules vivante
        #Créer un objet "cellules malades"
        for position in self.alive_map:
            cell = self.map[position[0]][position[1]]

            if cell.sick:
                #On boucle sur toutes les maladies de la cellule malade
                for id, d in cell.disease.items():
                    if not d.immun:
                        d.temps_malade += 1

                    #Si la maladie atteint le temps d'incubation, on jette un dé
                    if d.temps_malade >= d.incubation_time:
                        #roll a dice
                        dice = random.random()

                        #Le dé fait moins que la létalité : la cellule meurs
                        if dice < d.letalite:

                            #Ce try except est là au cas où on voudrat retiré de la carte une cellule déjà morte
                            # (tué par deux maladies en même temps)
                            try:
                                self.alive_map.remove(cell.location)
                                self.dead_cell.append([id, cell.location])
                            except:
                                pass

                            #On reset la cellule pour la tuer
                            cell.reset()

                        #Le dé fait plus que la létalité : la cellule devient immunisé pour cette maladie
                        #et n'est plus malade
                        else:
                            d.immun = True
                            d.temps_malade = 0

                    #Si la cellule est immunisé pour toutes les maladies qu'elle a attrapé,
                    # alors elle n'est plus malade
                    all_immun_statut = [i.immun for i in cell.disease.values()]
                    if not False in all_immun_statut:
                        cell.sick = False

class Disease:
    def __init__(self, image):
        self.id = make_random_id()
        self.incubation_time = random.randint(incubation_min, incubation_max)
        self.letalite = random.uniform(letalité_min, letalité_max)
        self.immun = False
        self.temps_malade = 0
        self.image = image
        self.contagiosité = random.uniform(contagiosité_min, contagiosité_max)

    def __getdiseasestate__(self):
        d = self.__dict__
        self_dict = {k : d[k] for k in d}
        return self_dict

    def __setstate__(self, state):
        self.__dict__ = state


def make_some_random_disease(n):
    all_disease = {}
    all_images = ["random_image/"+i for i in os.listdir("random_image") if ".png" in i]

    for i in range(n):
        d = Disease(all_images[i])
        all_disease[d.id] = d

    return all_disease