from core.pheromone_grid import PheromoneGrid
from config import *
import numpy as np


class Environment:

    def __init__(self, pheromone_grids, nest, food_grid, ants):
        self.pheromone_grids = pheromone_grids
        self.nest = nest
        self.food_grid = food_grid
        self.ants = ants
        self.display_mode = 1

    def get_x_y(self):
        return self.nest.get_x_y()

    def update_environment(self):
        self.pheromone_grids.update_pheromone()
        self.food_grid.update()

    def step(self):
        
        self.update_environment()

        for ant in self.ants:
            delta_theta = np.random.uniform(-RANDOM_DIR, RANDOM_DIR)
            p_type_deposit = PheromoneGrid.FOOD if ant.food_carried > TRESHOLD_FOOD else PheromoneGrid.HOME
            p_type_follow = PheromoneGrid.HOME if ant.food_carried > TRESHOLD_FOOD else PheromoneGrid.FOOD

            (lx, ly), (rx, ry), (fx, fy) = ant.get_antenna_pos()
            left_pheromone = self.pheromone_grids.get_pheromone(p_type_follow, lx, ly)
            right_pheromone = self.pheromone_grids.get_pheromone(p_type_follow, rx, ry)
            front_pheromone = self.pheromone_grids.get_pheromone(p_type_follow, fx, fy)

            if front_pheromone >= left_pheromone and front_pheromone >= right_pheromone :
                bias = 0
            elif left_pheromone > right_pheromone :
                 bias = ANTENNA_WEIGHT*(left_pheromone - right_pheromone)
            else : 
                bias = -ANTENNA_WEIGHT*(right_pheromone - left_pheromone)

            total_delta = np.clip(delta_theta + bias, -LIM_ANGLE, LIM_ANGLE) # on limite le changement de direction pour eviter les changements brusques qui font tourner en rond

            old_x, old_y = ant.move(total_delta)

            self.pheromone_grids.add_pheromones(p_type_deposit, round(old_x), round(old_y), ant.pheromone_deposit)

            source = self.food_grid.get_source(round(ant.x), round(ant.y))
            deposited = ant.interact(source, ant.is_at_nest(self.nest))
            if deposited > 0:
                self.nest.food_collected += deposited
