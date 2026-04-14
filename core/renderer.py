from pygame import surface

from core.pheromone_grid import PheromoneGrid
from config import *
import numpy as np
from core.food_source import FoodSource


class Renderer:

    def render(self, env, display_mode):
        if display_mode == 1 : 
            surface = self._get_pheromone_surface(env.pheromone_grids)
        elif display_mode == 2 :
            surface = self._get_pheromone_home_surface(env.pheromone_grids)
        elif display_mode == 3 :
            surface = self._get_pheromone_food_surface(env.pheromone_grids)

        food_surface = self._get_food_surface(env.food_grid)
        food_mask = np.any(food_surface != 0, axis=2)
        surface[food_mask] = food_surface[food_mask]

        dy, dx = np.ogrid[-ANT_RADIUS:ANT_RADIUS+1, -ANT_RADIUS:ANT_RADIUS+1]
        ant_mask = dx**2 + dy**2 <= ANT_RADIUS**2

        for ant in env.ants:
            ax, ay = int(ant.x), int(ant.y)
            color = COLOR_ANT_FOOD if ant.food_carried > TRESHOLD_FOOD else COLOR_ANT_HOME
            y0, y1 = max(ay - ANT_RADIUS, 0), min(ay + ANT_RADIUS + 1, GRID_HEIGHT)
            x0, x1 = max(ax - ANT_RADIUS, 0), min(ax + ANT_RADIUS + 1, GRID_WIDTH)
            local_mask = ant_mask[y0-ay+ANT_RADIUS : y1-ay+ANT_RADIUS, x0-ax+ANT_RADIUS : x1-ax+ANT_RADIUS]
            surface[y0:y1, x0:x1][local_mask] = color
            
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
    
    def _get_pheromone_home_surface(self, pheromone_grids) : 
        rh, gh, bh = COLOR_HOME 
        rgb = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3))

        home = pheromone_grids.get_pheromone_type(PheromoneGrid.HOME)
        home_mask = home > 0 

        rgb[:, :, 0] = np.where(home_mask, home*rh, 0) 
        rgb[:, :, 1] = np.where(home_mask, home*gh, 0)
        rgb[:, :, 2] = np.where(home_mask, home*bh, 0)

        return rgb.astype(np.uint8)
    
    def _get_pheromone_food_surface(self, pheromone_grids) : 
        rf, gf, bf = COLOR_FOOD
        rgb = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3))

        food = pheromone_grids.get_pheromone_type(PheromoneGrid.FOOD)
        food_mask = food > 0

        rgb[:, :, 0] = np.where(food_mask, food * rf, 0)
        rgb[:, :, 1] = np.where(food_mask, food * gf, 0)
        rgb[:, :, 2] = np.where(food_mask, food * bf, 0)

        return rgb.astype(np.uint8)


    def _get_food_surface(self, food_grid):
        ra, ga, ba = COLOR_APHID
        rs, gs, bs = COLOR_SUGAR
        rgb = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3))
        dy, dx = np.ogrid[-FOOD_RADIUS:FOOD_RADIUS+1, -FOOD_RADIUS:FOOD_RADIUS+1]
        food_mask = dx**2 + dy**2 <= FOOD_RADIUS**2

        for source in food_grid.sources:

            color = COLOR_APHID if source.type_food == FoodSource.APHID else COLOR_SUGAR
            x, y = source.x, source.y 
            y0, y1 = max(y - FOOD_RADIUS, 0), min(y + FOOD_RADIUS + 1, GRID_HEIGHT)
            x0, x1 = max(x - FOOD_RADIUS, 0), min(x + FOOD_RADIUS + 1, GRID_WIDTH)
            local_mask = food_mask[y0-y+FOOD_RADIUS:y1-y+FOOD_RADIUS,x0-x+FOOD_RADIUS:x1-x+FOOD_RADIUS]
            rgb[y0:y1, x0:x1][local_mask] = [c*source.quantity for c in color]

        return rgb.astype(np.uint8)

    def _get_nest_surface(self, nest):
        if nest is None : 
            return np.zeros((GRID_HEIGHT, GRID_WIDTH, 3), dtype=np.uint8)
        surface = np.zeros((GRID_HEIGHT, GRID_WIDTH, 3))
        x, y = nest.get_x_y()
        dy, dx = np.ogrid[-NEST_RADIUS:NEST_RADIUS+1, -NEST_RADIUS:NEST_RADIUS+1]
        mask = dx**2 + dy**2 <= NEST_RADIUS**2
        surface[y-NEST_RADIUS:y+NEST_RADIUS+1, x-NEST_RADIUS:x+NEST_RADIUS+1][mask] = COLOR_NEST
        return surface.astype(np.uint8)

