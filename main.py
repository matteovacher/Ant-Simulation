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
from map.manage_map import load_map

def rules() : 
    print("\n --- RULES --- \n")
    print(" Here are the rules of the simulation control : \n")
    print(" - Press Q to display the strongest pheromone between HOME and FOOD")
    print(" - Press S to display only the HOME pheromone")
    print(" - Press D to display only the FOOD pheromone")
    print(" - Click with the left mouse button to add an APHID food source at the clicked location")
    print(" - Click with the right mouse button to add a SUGAR food source at the clicked location")
    print("\n To close the simulation, simply click on the close button of the window\n")
    print(" --- END --- \n")

if __name__ == "__main__" :

    pheromone_grids = PheromoneGrid()

    rules()
    food_grid, nest = load_map() 

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Simulation Grid")
    clock = pygame.time.Clock()
    running = True 

    ants = [Ant(nest.x, nest.y, ANGLE_ANTENNA, LENGTH_ANTENNA) for i in range(N_ANTS)]

    env = Environment(pheromone_grids, nest, food_grid, ants) # emplacement du nid au milieu
    renderer = Renderer()

    font = pygame.font.SysFont("monospace", 20)

    while running : 

        for event in pygame.event.get() : 
            if event.type == pygame.QUIT : 
                running = False
            elif event.type == pygame.KEYDOWN : 
                if event.key == pygame.K_q : 
                    env.display_mode = 1
                elif event.key == pygame.K_s : 
                    env.display_mode = 2
                elif event.key == pygame.K_d : 
                    env.display_mode = 3

        tf.mouse_brush(food_grid)
        
        screen.fill("black")

        env.step() 

        env_surface = renderer.render(env, env.display_mode)

        actual_surface = pygame.surfarray.make_surface(np.transpose(env_surface, (1, 0, 2)))

        actual_surface = pygame.transform.scale(actual_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(actual_surface, (0,0))

        text = font.render(f"Food collected : {env.nest.food_collected:.2f}", True, (255, 255, 255))

        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit() 


