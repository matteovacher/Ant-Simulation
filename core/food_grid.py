from config import *
import numpy as np
from core.food_source import FoodSource

class FoodGrid:

    def __init__(self, food_sources):
        self.sources = food_sources
        self.grid = np.zeros((N_FOOD_TYPES, GRID_HEIGHT, GRID_WIDTH))
        self.proximity_map= {}
        self._build_grid()
        self._build_proximity_map()

    def _build_grid(self):
        for source in self.sources : 
            self.grid[source.type_food, source.y, source.x] = source.quantity

    def _build_proximity_map(self) :
        for source in self.sources : 
            for x in range(max(0, source.x - FOOD_RADIUS), min(GRID_WIDTH, source.x + FOOD_RADIUS + 1)) : 
                for y in range(max(0, source.y - FOOD_RADIUS), min(GRID_HEIGHT, source.y + FOOD_RADIUS + 1)) : 
                    if source.distance(x, y) <= FOOD_RADIUS :
                        if (x, y) not in self.proximity_map : 
                            self.proximity_map[(x, y)] = source 

    def add_source(self, source) : 
        self.sources.append(source)
        self.grid[source.type_food, source.y, source.x] = source.quantity
        for x in range(max(0, source.x - FOOD_RADIUS), min(GRID_WIDTH, source.x + FOOD_RADIUS + 1)) : 
            for y in range(max(0, source.y - FOOD_RADIUS), min(GRID_HEIGHT, source.y + FOOD_RADIUS + 1)) : 
                if source.distance(x, y) <= FOOD_RADIUS :
                    self.proximity_map[(x, y)] = source

    def update(self):
        for source in self.sources : 
            if source.type_food == FoodSource.SUGAR and source.quantity == 0 :
                continue
            source.recharge() 
            self.grid[source.type_food, source.y, source.x] = source.quantity 


    def get_source(self, x, y) : 
        return self.proximity_map.get((x, y), None)



