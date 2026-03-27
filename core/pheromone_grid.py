from config import * 
import numpy as np
from scipy.ndimage import gaussian_filter


class PheromoneGrid : 

    HOME = 0
    FOOD = 1
    def __init__(self) : 
        # ici le 0 c'est le home ie retour et 1 c'est vers nouriture 
        self.grids = np.zeros((2, GRID_HEIGHT, GRID_WIDTH))

    def get_pheromone(self, type_of_pheromone, x, y) : 
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT : 
            raise ValueError(f"Position ({x}, {y}) hors des limites de la grille")
        return self.grids[type_of_pheromone, y, x]
    
    def get_pheromone_type(self, type_of_pheromone) : 
        return self.grids[type_of_pheromone]
    
    def set_pheromone(self, type_of_pheromone, x, y, value) : 
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT : 
            raise ValueError(f"Position ({x}, {y}) hors des limites de la grille")
        self.grids[type_of_pheromone, y, x] = value

    def update_pheromone(self) : 
        # d'abord on considere l'evaporation des pheromones 
        self.grids *= EVAPORATION_RATE

        # ensuite on procede a la diffusion 
        gaussian_filter(self.grids, # la matrice a transfo 
                        sigma = DIFFUSION_SIGMA, # le rayonnement ie si grand ca s'etale bcp cf diffusion physique 
                        order = 0, # pas de dérivé 
                        output = self.grids, # efficacité memoire modif direct sur la grille sans nouvelle alloc memoire 
                        mode = 'constant', # ici on arrete le monde au bord sans rebond 
                        cval = 0.0, # val a l'ext ici nul au dela de la limite  
                        truncate = 6.0, 
                        radius = None, # jsute calcul via sigma  
                        axes = (1,2) # applique en 2D
                        ) 

        # si la valeur est trop faible on la met à 0 
        self.grids[self.grids < 0.0001] = 0 

    def add_pheromones(self, type_of_pheromone, x, y, value) :
        if value < 0 or value > 1 :
            raise ValueError(f"La valeur de phéromone doit etre comprise entre 0 et 1")
        # on verif que la case est dans les limites de la grille 
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT : 
            raise ValueError(f"Position ({x}, {y}) hors des limites de la grille")
        self.grids[type_of_pheromone, y, x] += value



