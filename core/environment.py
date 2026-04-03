from core.pheromone_grid import PheromoneGrid
from config import *
import numpy as np
from core.nest import Nest
from core.food_grid import FoodGrid

class Environment : 

    def __init__(self, pheromone_grids, nest, food_grid) : 
        self.pheromone_grids = pheromone_grids
        self.nest = nest
        self.food_grid = food_grid


    def get_x_y(self) : 
        return self.nest.get_x_y()
    
    def update_environnement(self) : 
        self.pheromone_grids.update_pheromone()
        self.food_grid.update()

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
    
    def get_nest_surface(self) : 
        surface = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3))
        x, y = self.nest.get_x_y()
        dy, dx = np.ogrid[-NEST_RADIUS:NEST_RADIUS+1, -NEST_RADIUS:NEST_RADIUS+1]
        mask = dx**2 + dy**2 <= NEST_RADIUS**2
        surface[y-NEST_RADIUS:y+NEST_RADIUS+1, x-NEST_RADIUS:x+NEST_RADIUS+1][mask] = COLOR_NEST
        return surface.astype(np.uint8)  

    def get_food_surface(self) :
        return self.food_grid.get_food_surface()  


