from core.pheromone_grid import PheromoneGrid
from config import *
import numpy as np
from core.nest import Nest
from core.food_grid import FoodGrid
from core.ant import Ant 

class Environment : 

    def __init__(self, pheromone_grids, nest, food_grid, ants) : 
        self.pheromone_grids = pheromone_grids
        self.nest = nest
        self.food_grid = food_grid
        self.ants = ants 


    def get_x_y(self) : 
        return self.nest.get_x_y()
    
    def update_environment(self) : 
        self.pheromone_grids.update_pheromone()
        self.food_grid.update()

    def step(self) : 
        self.update_environment()

        env_surface = self.get_pheromone_surface() 

        env_food = self.get_food_surface()
        food_mask = np.any(env_food != 0, axis = 2)
        env_surface[food_mask] = env_food[food_mask]

        for ant in self.ants : 
            delta_theta = np.random.uniform(-np.pi/6, np.pi/6) # on ajoute un peu de bruit pour eviter les comportements trop deterministes
            old_x, old_y = ant.move(delta_theta)
            p_type = PheromoneGrid.FOOD if ant.has_food else PheromoneGrid.HOME
            self.pheromone_grids.add_pheromones(p_type, old_x, old_y, PHEROMONE_DEPOSIT)

            source = self.food_grid.get_source(int(ant.x), int(ant.y))
            deposited = ant.interact(source, ant.is_at_nest(self.nest))
            if deposited : 
                self.nest.food_collected += 1

            env_surface[int(ant.y), int(ant.x)] = COLOR_ANT # on affiche les fourmis en orange 

        env_nest = self.get_nest_surface()
        nest_mask = np.any(env_nest != 0, axis = 2)
        env_surface[nest_mask] = env_nest[nest_mask] 

        return env_surface    




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


