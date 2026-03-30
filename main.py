from core.environment import Environment
from core.pheromone_grid import PheromoneGrid
from config import *
import pygame
import numpy as np 
import tests.tests_pheromones as tp 
from core.nest import Nest

if __name__ == "__main__" :

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Simulation Grid")
    clock = pygame.time.Clock()

    pheromone_grids = PheromoneGrid()
    nest = Nest(NEST_X, NEST_Y)
    env = Environment(pheromone_grids, nest) # emplacement du nid au milieu

    running = True 

    while running : 

        for event in pygame.event.get() : 
            if event.type == pygame.QUIT : 
                running = False
            
        tp.mouse_brush(pheromone_grids)
        
        screen.fill("black")

        env.update_environnement()
        env_surface = env.get_pheromone_surface()
        env_nest = env.get_nest_surface()
        nest_mask = np.any(env_nest != 0, axis = 2)

        env_surface[nest_mask] = env_nest[nest_mask]

        actual_surface = pygame.surfarray.make_surface(np.transpose(env_surface, (1, 0, 2)))

        actual_surface = pygame.transform.scale(actual_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(actual_surface, (0,0))

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit() 


