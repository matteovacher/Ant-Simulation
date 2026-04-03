import pygame 
from config import *
from core.food_grid import FoodGrid  
from core.food_source import FoodSource

def convert_scale(mx, my) : 

    x_on_grid = int(mx * (GRID_WIDTH/WINDOW_WIDTH) )
    y_on_grid = int(my * (GRID_HEIGHT/WINDOW_HEIGHT))
    
    return x_on_grid, y_on_grid

def mouse_brush(food_sources) :
    buttons = pygame.mouse.get_pressed()
    if buttons[0] : 
        mx, my = pygame.mouse.get_pos()
        x_on_grid, y_on_grid = convert_scale(mx, my)
        if any(source.x == x_on_grid and source.y == y_on_grid for source in food_sources):
            print("DEBUG : source de nourriture déjà présente à cet emplacement")
        elif 0 <= x_on_grid < GRID_WIDTH and 0 <= y_on_grid < GRID_HEIGHT :
            food_sources.append(FoodSource(FoodSource.APHID, x_on_grid, y_on_grid, quantity = 1, recharge_rate = RECHARGE_RATE_APHID))
        else : 
            print("DEBUG : clic hors grille")
    elif buttons[2] : 
        mx, my = pygame.mouse.get_pos()
        x_on_grid, y_on_grid = convert_scale(mx, my)
        if any(source.x == x_on_grid and source.y == y_on_grid for source in food_sources):
            print("DEBUG : source de nourriture déjà présente à cet emplacement")
        elif 0 <= x_on_grid < GRID_WIDTH and 0 <= y_on_grid < GRID_HEIGHT:
            food_sources.append(FoodSource(FoodSource.SUGAR, x_on_grid, y_on_grid, quantity = 1, recharge_rate = RECHARGE_RATE_SUGAR))
        else : 
            print("DEBUG : clic hors grille")