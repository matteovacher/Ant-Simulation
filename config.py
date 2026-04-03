import numpy as np 

# grille et pheromones 

EVAPORATION_RATE = 0.999   # entre 0 et 1 on def une suite geo 
GRID_WIDTH = 360     # largeur de la grille en case 
GRID_HEIGHT = 240       # hauteur de la grille aussi en case 
DIFFUSION_SIGMA = 0.3    # pour la diffusion des pheromones et scipy 
CELL_SIZE = 3           # taille de la case en pixels
FPS = 24                # images par seconde
WINDOW_WIDTH = GRID_WIDTH*CELL_SIZE       # largeur de la fenetre = width*cellsize (2880 pixels max )
WINDOW_HEIGHT = GRID_HEIGHT*CELL_SIZE     # hauteur de la fenetre = height*cellsize (1920 pixels max )
PHEROMONE_DEPOSIT = 0.7 

# env
#  
COLOR_HOME = (139, 90, 43) # couleur marron 
COLOR_FOOD = (50, 205, 50) # couleur vert 
COLOR_BACKGROUND = (0, 0, 0) # couleur noir 
COLOR_NEST = (255, 255, 255) # couleur blanc 
NEST_RADIUS = 2 # rayon du nid 
NEST_X = 100    # coordonnees du nid
NEST_Y = 100    # coordonnees du nid

# ant 
LENGTH_ANTENNA = 0.5 # longueur de l'antenne en cases
ANGLE_ANTENNA = np.pi/4 # angle entre la direction de l'antenne et la direction de l'ant (en radians)
N_ANTS = 20 
COLOR_ANT = (255, 165, 0) # couloeur orange 

# food 
N_FOOD_TYPES = 2 
COLOR_APHID = (255, 220, 0) # couleur jaune
COLOR_SUGAR = (100, 200, 255) # bleu 
RECHARGE_RATE_APHID = 0.01
RECHARGE_RATE_SUGAR = 0

