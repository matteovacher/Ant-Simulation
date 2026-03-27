import pygame 
from config import *
from core.pheromone_grid import PheromoneGrid

def convert_scale(mx, my) : 

    x_on_grid = int(mx * (GRID_WIDTH/WINDOW_WIDTH) )
    y_on_grid = int(my * (GRID_HEIGHT/WINDOW_HEIGHT))
    
    return x_on_grid, y_on_grid


def mouse_brush(pheromone_grids) : 

    buttons = pygame.mouse.get_pressed()
    if buttons[0] or buttons[2] :
        mx , my = pygame.mouse.get_pos()
        x_on_grid, y_on_grid = convert_scale(mx, my)

        if 0 <= x_on_grid < GRID_WIDTH and 0 <= y_on_grid < GRID_HEIGHT:
            if buttons[0] : # si clic gauche 
                pheromone_grids.add_pheromones(PheromoneGrid.HOME, x_on_grid, y_on_grid, value = 1)
            elif buttons[2] : # si clic droit 
                pheromone_grids.add_pheromones(PheromoneGrid.FOOD, x_on_grid, y_on_grid, value = 1)
        else : 
            print("DEBUG : clic hors grille")

# def mouse_action(event, pheromone_grids) : 
    
#     if event.type == pygame.MOUSEBUTTONDOWN : # si pression 
#         mx, my = pygame.mouse.get_pos()
#         x_on_grid, y_on_grid = convert_scale(mx, my)

#         if event.button == 1 : # si clic gauche 
#             print(f"DEBUG : clic gauche à mx = {mx}, my = {my}, x_on_grid = {x_on_grid}, y_on_grid = {y_on_grid}")
#             if (0 <= x_on_grid < GRID_WIDTH and 0 <= y_on_grid < GRID_HEIGHT):
#                 pheromone_grids.add_pheromones(PheromoneGrid.HOME, x_on_grid, y_on_grid, value = 1)
#             else : 
#                 print("DEBUG : clic gauche hors grille")


#         elif event.button == 3 : # si clic droit 
#             print(f"DEBUG : clic droit à mx = {mx}, my = {my}, x_on_grid = {x_on_grid}, y_on_grid = {y_on_grid}")
#             if (0 <= x_on_grid < GRID_WIDTH and 0 <= y_on_grid < GRID_HEIGHT):
#                 pheromone_grids.add_pheromones(PheromoneGrid.FOOD, x_on_grid, y_on_grid, value = 1)
#             else : 
#                 print("DEBUG : clic droit hors grille")
        

