from config import * 
import numpy as np
from scipy.ndimage import gaussian_filter


class PheromoneGrid : 

    HOME = 0
    FOOD = 1
    def __init__(self) : 
        # ici le 0 c'est le home ie retour et 1 c'est vers nouriture 
        self.grids = np.zeros((2, GRID_HEIGHT, GRID_WIDTH))

    def get_pheromone(self, type_of_pheromone x, y) : 
        return self.grids[type_of_pheromone, y, x]
    
    def set_pheromone(self, type_of_pheromone, x, y, value) : 
        self.grids[type_of_pheromone, y, x] = value

    def update_pheromone(self) : 
        # d'abord on considere l'evaporation des pheromones 
        self.grids *= EVAPORATION_RATE

        # ensuite on procede a la diffusion 
        gaussian_filter(self.grids, # la matrice a transfo 
                        sigma = DIFFUSION_SIGMA, # le rayonnement ie si grand ca s'etale bcp cf diffusion physique 
                        order = 0, # pas de dérivé 
                        orutput = self.grids, # efficacité memoire modif direct sur la grille sans nouvelle alloc memoire 
                        mode = 'constant', # ici on arrete le monde au bord sans rebond 
                        cval = 0, # val a l'ext ici nul le                         truncate = 4.0, 
                        radius = None, # jsute calcul via sigma  
                        axes = (1,2) # applique en 2D
                        ) 

        # si la valeur est trop faible on la met à 0 
        self.grids[self.grid < 0.01] = 0 

    def add_pheromones(self, x, y, value) :
        # on verif que la case est dans les limites de la grille 
        #  
        self.grids[y, x] += value



