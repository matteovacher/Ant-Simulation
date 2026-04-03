from core.environment_bis import Environment 
from core.renderer import Renderer 
from core.food_grid import FoodGrid
from core.pheromone_grid import PheromoneGrid
from core.food_source import FoodSource
from config import *
import pygame
import numpy as np 
import tests.tests_food as tf 
from core.nest import Nest
from core.ant import Ant 

if __name__ == "__main__" :

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Simulation Grid")
    clock = pygame.time.Clock()

    pheromone_grids = PheromoneGrid()
    nest = Nest(NEST_X, NEST_Y)
    food_grid = FoodGrid([])

    running = True 

    ants = [Ant(NEST_X, NEST_Y, ANGLE_ANTENNA, LENGTH_ANTENNA) for i in range(N_ANTS)]

    env = Environment(pheromone_grids, nest, food_grid, ants) # emplacement du nid au milieu
    renderer = Renderer()

    while running : 

        for event in pygame.event.get() : 
            if event.type == pygame.QUIT : 
                running = False
            
        tf.mouse_brush(food_grid)
        
        screen.fill("black")

        env.step()
        env_surface = renderer.render(env)

        actual_surface = pygame.surfarray.make_surface(np.transpose(env_surface, (1, 0, 2)))

        actual_surface = pygame.transform.scale(actual_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(actual_surface, (0,0))

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit() 


