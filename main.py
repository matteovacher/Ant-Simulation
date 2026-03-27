from core.environment import Environment
from core.pheromone_grid import PheromoneGrid
from config import *
import pygame
import numpy as np 
import tests.tests_pheromones as tp 

if __name__ == "__main__" :

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Simulation Grid")
    clock = pygame.time.Clock()

    pheromone_grids = PheromoneGrid()
    env = Environment(pheromone_grids, GRID_WIDTH//2, GRID_HEIGHT//2) # emplacement du nid au milieu

    running = True 

    while running : 

        for event in pygame.event.get() : 
            if event.type == pygame.QUIT : 
                running = False
            
        tp.mouse_brush(pheromone_grids)
        
        screen.fill("black")

        env.update_environnement()
        env_surface = env.get_pheromone_surface()


        actual_surface = pygame.surfarray.make_surface(np.transpose(env_surface, (1, 0, 2)))
        actual_surface = pygame.transform.scale(actual_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(actual_surface, (0,0))

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit() 


