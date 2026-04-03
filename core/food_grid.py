from config import *
import numpy as np
from core.food_source import FoodSource

class FoodGrid:

    def __init__(self, food_sources):
        self.sources = food_sources
        self.grid = np.zeros((N_FOOD_TYPES, GRID_HEIGHT, GRID_WIDTH))
        self._build_grid()

    def _build_grid(self):
        for source in self.sources : 
            self.grid[source.type_food, source.y, source.x] = source.quantity

    def update(self):
        for source in self.sources : 
            source.recharge()
            self.grid[source.type_food, source.y, source.x] = source.quantity

    def get_food_surface(self):
        ra, ga, ba = COLOR_APHID
        rs, gs, bs = COLOR_SUGAR

        rgb = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3))

        aphid = self.grid[FoodSource.APHID]
        sugar = self.grid[FoodSource.SUGAR]

        aphid_stronger = aphid > sugar

        red_array = np.where(aphid_stronger, aphid*ra, sugar*rs)
        green_array = np.where(aphid_stronger, aphid*ga, sugar*gs)
        blue_array = np.where(aphid_stronger, aphid*ba, sugar*bs)

        rgb[:, :, 0] = red_array
        rgb[:, :, 1] = green_array
        rgb[:, :, 2] = blue_array

        return rgb.astype(np.uint8) 

    def get_source(self, x, y) : 
        for source in self.sources : 
            if source.x == x and source.y == y : 
                return source
        return None



