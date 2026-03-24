# grille et pheromones 

EVAPORATION_RATE = 0.90   # entre 0 et 1 on def une suite geo 
GRID_WIDTH = 360     # largeur de la grille en case 
GRID_HEIGHT = 240       # hauteur de la grille aussi en case 
DIFFUSION_SIGMA = 1     # pour la diffusion des pheromones et scipy 
CELL_SIZE = 5           # taille de la case en pixels
FPS = 24                # images par seconde
WINDOW_WIDTH = GRID_WIDTH*CELL_SIZE       # largeur de la fenetre = width*cellsize (2880 pixels max )
WINDOW_HEIGHT = GRID_HEIGHT*CELL_SIZE     # hauteur de la fenetre = height*cellsize (1920 pixels max )


# env
#  
COLOR_HOME = (139, 90, 43) # couleur marron 
COLOR_FOOD = (50, 205, 50) # couleur vert 
COLOR_BACKGROUND = (0, 0, 0) # couleur noir 