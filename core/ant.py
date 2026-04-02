from config import *
import numpy as np
from core.pheromone_grid import PheromoneGrid

class Ant : 

    def __init__(self, x, y, grids, angle_antenna, length_antenna ) :

        self.x = x
        self.y = y 
        self.has_food = False 
        self.is_home = True 
        self.pheromone_grid = grids
        self.direction = np.random.uniform(0, 2*np.pi) # direction initiale aleatoire
        self.angle_antenna = angle_antenna
        self.length_antenna = length_antenna  # longueur de l'antenne en cases

    def move(self,delta_theta,  put_pheromones, value_pheromone) : 
        self.direction += delta_theta
        new_x = self.x + np.cos(self.direction) # pas de temps de 1 et vitesse de 1 case 
        new_y = self.y + np.sin(self.direction)
        
        # on verifie que les valeurs ne sortent pas de smurs 
        x_clipped = np.clip(new_x, 0, GRID_WIDTH-1)
        y_clipped = np.clip(new_y, 0, GRID_HEIGHT-1)
        
        if x_clipped != new_x : 
            # si on sort de la grille on rebondit en inversant la direction 
            self.direction = np.pi - self.direction # on choisit une nouvelle direction aleatoire pour eviter de rester coincé au bord
        if y_clipped != new_y : 
            self.direction = -self.direction

        if put_pheromones : 
            if self.has_food : 
                self.pheromone_grid.add_pheromones(PheromoneGrid.FOOD, int(self.x), int(self.y), value_pheromone)
            else : 
                self.pheromone_grid.add_pheromones(PheromoneGrid.HOME, int(self.x), int(self.y), value_pheromone)

        self.x = x_clipped
        self.y = y_clipped 

    
    def get_antenna_pos(self) : 
        return [(self.x + self.length_antenna*np.cos(self.direction + self.angle_antenna), self.y + self.length_antenna*np.sin(self.direction + self.angle_antenna)), (self.x + self.length_antenna*np.cos(self.direction - self.angle_antenna), self.y + self.length_antenna*np.sin(self.direction - self.angle_antenna))] 




