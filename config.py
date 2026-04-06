import numpy as np 

# GRID AND PHEROMONE 

EVAPORATION_RATE = 0.999                # between 0 and 1, the higher the slower the evaporation
DIFFUSION_SIGMA = 0.35                   # between 0 and inf, the higher the more the pheromone spreads, but also the more it evaporates
GRID_WIDTH = 480                        # width of the grid in cells, also in pixels if cell size is 1, max 2880 for 8k screen
GRID_HEIGHT = 320                       # height of the grid in cells, also in pixels if cell size is 1, max 1920 for 8k screen
CELL_SIZE = 2                           # size of each cell in pixels
FPS = 60                                # frames per second
WINDOW_WIDTH = GRID_WIDTH*CELL_SIZE     # width of the window = width*cellsize (2880 pixels max )
WINDOW_HEIGHT = GRID_HEIGHT*CELL_SIZE   # height of the window = height*cellsize (1920 pixels max )
PHEROMONE_DEPOSIT = 0.8                 # amount of pheromone deposited by an ant at each step, between 0 and 1

# ENVIRONMENT
COLOR_HOME = (139, 90, 43)              # brown color for the pheromone leading to the nest
COLOR_FOOD = (50, 205, 50)              # green color for the pheromone leading to the food
COLOR_BACKGROUND = (0, 0, 0)            # black color for the background
COLOR_NEST = (255, 255, 255)            # white color for the nest
NEST_RADIUS = 10                        # radius of the nest in cells
NEST_X = int(GRID_WIDTH/2)              # coordinates of the nest, must be an integer 
NEST_Y = int(GRID_HEIGHT/2)             # coordinates of the nest, must be an integer 

# ANT
N_ANTS = 60                             # number of ants in the simulation, must be an integer greater than 0
LENGTH_ANTENNA = 0.5                    # length from the head to the tip of the antenna in cells, must be greater than 0
ANGLE_ANTENNA = np.pi/4                 # angle between the direction of the ant and the direction of the antenna in radians, between 0 and pi/2, if 0 then antennas are in the same direction as the ant, if pi/2 then antennas are perpendicular to the direction of the ant
COLOR_ANT = (255, 165, 0)               # orange color for the ants
MAX_FOOD_CARRIED = 0.5                  # maximum amount of food an ant can carry, between 0 and 1, if 0.5 then an ant can carry half of a food source
FOOD_COLLECT_AMOUNT = 0.5               # amount of food an ant can collect at one time, between 0 and MAX_FOOD_CARRIED
EAT_DURATION = 8                        # number of steps an ant needs to eat a food source, during this time the ant cannot move or interact with other food sources, must be an integer
ANTENNA_WEIGHT = np.pi/6                # weight of the pheromone bias on the ant's direction, between 0 and pi/2, if 0 then the ant ignores the pheromones, if pi/2 then the ant turns directly towards the strongest pheromone
TRESHOLD_FOOD = 0.45                    # threshold of food carried for an ant to switch from following home pheromone to following food pheromone, between 0 and MAX_FOOD_CARRIED
RANDOM_DIR = np.pi/10                   # maximum random change in direction for an ant at each step, between 0 and pi, if 0 then the ant never changes direction randomly, if pi then the ant can turn in any direction at each step
HALF_LENGTH_BODY = 0.5                  # half of the length of the ant's body in cells, used for drawing the ant as a line before adding the antenna 

# FOOD SOURCES 
N_FOOD_TYPES = 2                        # number of different types of food sources, must be an integer greater than 0
COLOR_APHID = (255, 220, 0)             # color yellow for aphids, which are a type of food source that can recharge 
COLOR_SUGAR = (100, 200, 255)           # color blue for sugar, which is another type of food source that does not recharge
RECHARGE_RATE_APHID = 0.01              # recharge rate for aphids, between 0 and 1
RECHARGE_RATE_SUGAR = 0                 # recharge rate for sugar, must be 0 since sugar does not recharge
