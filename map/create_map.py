import pygame 
from config import *
from core.food_grid import FoodGrid
from core.food_source import FoodSource 
from core.nest import Nest
from core.renderer import Renderer
import os
import json
from core.environment_bis import Environment
import numpy as np

def convert_scale(mx, my) : 

    x_on_grid = int(mx * (GRID_WIDTH/WINDOW_WIDTH) )
    y_on_grid = int(my * (GRID_HEIGHT/WINDOW_HEIGHT))
    
    return x_on_grid, y_on_grid

def create_map(food_grid, nest) :
    buttons = pygame.mouse.get_pressed()
    if buttons[0] : 
        mx, my = pygame.mouse.get_pos()
        x_on_grid, y_on_grid = convert_scale(mx, my)
        if food_grid.get_source(x_on_grid, y_on_grid) is not None :
            print("DEBUG : source de nourriture déjà présente à cet emplacement")
        elif 0 <= x_on_grid < GRID_WIDTH and 0 <= y_on_grid < GRID_HEIGHT :
            food_grid.add_source(FoodSource(FoodSource.APHID, x_on_grid, y_on_grid, quantity = 1, recharge_rate = RECHARGE_RATE_APHID))
        else : 
            print("DEBUG : clic hors grille")
    elif buttons[2] :
        mx, my = pygame.mouse.get_pos()
        x_on_grid, y_on_grid = convert_scale(mx, my) 
        if food_grid.get_source(x_on_grid, y_on_grid) is not None : 
            print("DEBUG : source de nourriture déjà présente à cet emplacement")
        elif 0 <= x_on_grid < GRID_WIDTH and 0 <= y_on_grid < GRID_HEIGHT :
            food_grid.add_source(FoodSource(FoodSource.SUGAR, x_on_grid, y_on_grid, quantity = 1, recharge_rate = RECHARGE_RATE_SUGAR))
        else : 
            print("DEBUG : clic hors grille")
    elif buttons[1] and nest is None :
        mx, my = pygame.mouse.get_pos()
        x_on_grid, y_on_grid = convert_scale(mx, my)
        if 0 <= x_on_grid < GRID_WIDTH and 0 <= y_on_grid < GRID_HEIGHT :
            nest = Nest(x_on_grid, y_on_grid)
    return nest 


def ask_map(running) : 
    number = input("Enter the map number, the map will be save as map_number in the stock folder, if a map with this number already exists it will be overwritten, if you want to keep it, move it before creating the new map : ")
    running = True
    return number, running 

def ask_nest() : 
    x = int(input(f"\nEnter the x position of the nest, must be an integer between 0 and {GRID_WIDTH-1} : "))
    y = int(input(f"\nEnter the y position of the nest, must be an integer between 0 and {GRID_HEIGHT-1} : "))
    return x, y

def save_map(food_grid, nest, name, number, screen) :
    answer = input(f"\n Do you want to save the map as number {number} ? \n - [y] \n - [n] \n --> ")
    if answer == "y" : 
        base_dir = os.path.dirname(os.path.abspath(__file__))
        stock_dir = os.path.join(base_dir, "stock")
        if not os.path.exists(stock_dir) :
            os.makedirs(stock_dir)
        data = {
            "name" : name, 
            "nest" : {
                "x" : nest.x, 
                "y" : nest.y
            },
            "food_sources" : [{
                "type_food" : source.type_food, 
                "x" : source.x, 
                "y" : source.y, 
                "quantity" : source.quantity, 
                "recharge_rate" : source.recharge_rate
            } for source in food_grid.sources
            ]
        }

        with open(os.path.join(stock_dir, f"map_{number}.json"), "w") as f:
            json.dump(data, f)
        pygame.image.save(screen, os.path.join(stock_dir, f"map_{number}.png"))
    else : 
        print("\n Map not saved")


def map_creation_rules() : 
    print("\n --- HOW TO CREATE A MAP --- \n")
    print(" - First, you will be asked to enter a map number, the map will be saved as map_number in the stock folder, if a map with this number already exists it will be overwritten, if you want to keep it, move it before creating the new map")
    print(" - Then you have to place the nest, for that click with the middle mouse button on the desired location, you can only place it once, if you want to move it, you have to restart the map creation")
    print(" - Click with the left mouse button to add an APHID food source at the clicked location")
    print(" - Click with the right mouse button to add a SUGAR food source at the clicked location")
    print("\n To save and close the map creation, simply click on the close button of the window, you will be asked if you want to save the map or not\n")
    print(" --- END --- \n")

if __name__ == "__main__" :

    food_grid = FoodGrid([])
    nest = None
    running = False 
    renderer = Renderer()

    number, running = ask_map(running)
    pygame.init()
    nest = create_map(food_grid, nest)

    screen =pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Create Map")
    clock = pygame.time.Clock()

    while running : 
        for event in pygame.event.get() : 
            if event.type == pygame.QUIT:
                if nest is not None:
                    save_map(food_grid, nest, "map", number, screen)
                running = False

        nest = create_map(food_grid, nest)
        screen.fill("black")
        env_surface = renderer._get_food_surface(food_grid)
        nest_surface = renderer._get_nest_surface(nest)
        nest_mask = np.any(nest_surface != 0, axis=2)
        env_surface[nest_mask] = nest_surface[nest_mask]

        actual_surface = pygame.surfarray.make_surface(np.transpose(env_surface, (1, 0, 2)))
        actual_surface = pygame.transform.scale(actual_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(actual_surface, (0,0))
        pygame.display.flip()   
        clock.tick(FPS)

    pygame.quit()

