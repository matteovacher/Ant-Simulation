from core.pheromone_grid import PheromoneGrid
from config import *
import numpy as np


class Environment:

    def __init__(self, pheromone_grids, nest, food_grid, ants):
        self.pheromone_grids = pheromone_grids
        self.nest = nest
        self.food_grid = food_grid
        self.ants = ants

    def get_x_y(self):
        return self.nest.get_x_y()

    def update_environment(self):
        self.pheromone_grids.update_pheromone()
        self.food_grid.update()

    def step(self):
        self.update_environment()

        for ant in self.ants:
            delta_theta = np.random.uniform(-np.pi/6, np.pi/6)
            old_x, old_y = ant.move(delta_theta)
            p_type = PheromoneGrid.FOOD if ant.has_food else PheromoneGrid.HOME
            self.pheromone_grids.add_pheromones(p_type, old_x, old_y, PHEROMONE_DEPOSIT)

            source = self.food_grid.get_source(int(ant.x), int(ant.y))
            deposited = ant.interact(source, ant.is_at_nest(self.nest))
            if deposited:
                self.nest.food_collected += 1
