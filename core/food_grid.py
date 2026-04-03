from config import *
import numpy as np
from core.food_source import FoodSource

class FoodGrid:

    def __init__(self, food_sources):
        self.sources = food_sources
        self.grid = np.zeros((N_FOOD_TYPES, GRID_HEIGHT, GRID_WIDTH))
        self.source_map = {}
        self._build_grid()

    def _build_grid(self):
        for source in self.sources : 
            self.grid[source.type_food, source.y, source.x] = source.quantity
            self.source_map[(source.x, source.y)] = source

    def add_source(self, source) : 
        self.sources.append(source)
        self.grid[source.type_food, source.y, source.x] = source.quantity
        self.source_map[(source.x, source.y)] = source

    def update(self):
        for source in self.sources : 
            source.recharge()
            self.grid[source.type_food, source.y, source.x] = source.quantity

    def get_source(self, x, y) : 
        return self.source_map.get((x, y), None)



