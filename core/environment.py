from core.pheromone_grid import PheromoneGrid
from config import *
import numpy as np


class Environment : 

    def __init__(self, pheromone_grids, x_nest, y_nest) : 
        self.pheromone_grids = pheromone_grids
        self.x_nest = x_nest 
        self.y_nest = y_nest
        if self.x_nest < 0 or self.x_nest >= GRID_WIDTH or self.y_nest < 0 or self.y_nest >= GRID_HEIGHT : 
            raise ValueError(f"Position ({self.x_nest}, {self.y_nest}) hors des limites de la grille")

    def get_x_y(self) : 
        return self.x_nest, self.y_nest
    
    def update_environnement(self) : 
        self.pheromone_grids.update_pheromone()

    def get_pheromone_surface(self) : 
        rh, gh, bh = COLOR_HOME
        rf, gf, bf = COLOR_FOOD
        rgb = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3))

        home = self.pheromone_grids.get_pheromone_type(PheromoneGrid.HOME)
        food = self.pheromone_grids.get_pheromone_type(PheromoneGrid.FOOD)

        home_stronger = home > food

        red_array = np.where(home_stronger, home*rh, food*rf)
        green_array = np.where(home_stronger, home*gh, food*gf)
        blue_array = np.where(home_stronger, home*bh, food*bf)
        rgb[:, :, 0] = red_array
        rgb[:, :, 1] = green_array
        rgb[:, :, 2] = blue_array
        return rgb.astype(np.uint8)


