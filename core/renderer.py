from core.pheromone_grid import PheromoneGrid
from config import *
import numpy as np
from core.food_source import FoodSource


class Renderer:

    def render(self, env):
        surface = self._get_pheromone_surface(env.pheromone_grids)

        food_surface = self._get_food_surface(env.food_grid)
        food_mask = np.any(food_surface != 0, axis=2)
        surface[food_mask] = food_surface[food_mask]

        for ant in env.ants:
            surface[int(ant.y), int(ant.x)] = COLOR_ANT

        nest_surface = self._get_nest_surface(env.nest)
        nest_mask = np.any(nest_surface != 0, axis=2)
        surface[nest_mask] = nest_surface[nest_mask]

        return surface

    def _get_pheromone_surface(self, pheromone_grids):
        rh, gh, bh = COLOR_HOME
        rf, gf, bf = COLOR_FOOD
        rgb = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3))

        home = pheromone_grids.get_pheromone_type(PheromoneGrid.HOME)
        food = pheromone_grids.get_pheromone_type(PheromoneGrid.FOOD)
        home_stronger = home > food

        rgb[:, :, 0] = np.where(home_stronger, home * rh, food * rf)
        rgb[:, :, 1] = np.where(home_stronger, home * gh, food * gf)
        rgb[:, :, 2] = np.where(home_stronger, home * bh, food * bf)

        return rgb.astype(np.uint8)

    def _get_food_surface(self, food_grid):
        ra, ga, ba = COLOR_APHID
        rs, gs, bs = COLOR_SUGAR
        rgb = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3))

        aphid = food_grid.grid[FoodSource.APHID]
        sugar = food_grid.grid[FoodSource.SUGAR]
        aphid_stronger = aphid > sugar

        rgb[:, :, 0] = np.where(aphid_stronger, aphid * ra, sugar * rs)
        rgb[:, :, 1] = np.where(aphid_stronger, aphid * ga, sugar * gs)
        rgb[:, :, 2] = np.where(aphid_stronger, aphid * ba, sugar * bs)

        return rgb.astype(np.uint8)

    def _get_nest_surface(self, nest):
        surface = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3))
        x, y = nest.get_x_y()
        dy, dx = np.ogrid[-NEST_RADIUS:NEST_RADIUS+1, -NEST_RADIUS:NEST_RADIUS+1]
        mask = dx**2 + dy**2 <= NEST_RADIUS**2
        surface[y-NEST_RADIUS:y+NEST_RADIUS+1, x-NEST_RADIUS:x+NEST_RADIUS+1][mask] = COLOR_NEST
        return surface.astype(np.uint8)

