from config import *
import numpy as np

class Ant : 

    def __init__(self, x, y, angle_antenna, length_antenna ) :

        self.x = x
        self.y = y 
        self.food_carried = 0
        self.eating_timer = 0 
        self.direction = np.random.uniform(0, 2*np.pi) # direction initiale aleatoire
        self.angle_antenna = angle_antenna
        self.length_antenna = length_antenna  # longueur de l'antenne en cases
        self.pheromone_deposit = PHEROMONE_DEPOSIT
        self.nest_timer = 0 


    def move(self,delta_theta) : 
        if self.eating_timer > 0 : 
            self.eating_timer -= 1
            self.direction += np.pi if self.eating_timer == 0 else 0
            self.pheromone_deposit = PHEROMONE_DEPOSIT if self.eating_timer == 0 else 0
            return self.x, self.y # bouge pas tant que on mange 
        
        if self.nest_timer > 0 : 
            self.nest_timer -= 1
            self.pheromone_deposit = PHEROMONE_DEPOSIT if self.nest_timer == 0 else 0
            self.direction += np.pi if self.nest_timer == 0 else 0
            delta_theta = np.random.uniform(-NEST_ANGLE_VARIATION, NEST_ANGLE_VARIATION) if self.nest_timer == 1 else 0
            return self.x, self.y # bouge pas tant que on est au nid

        self.direction += delta_theta
        new_x = self.x + np.cos(self.direction) # pas de temps de 1 et vitesse de 1 case 
        new_y = self.y + np.sin(self.direction)
        
        # on verifie que les valeurs ne sortent pas de smurs 
        x_clipped = np.clip(new_x, 0, GRID_WIDTH-1)
        y_clipped = np.clip(new_y, 0, GRID_HEIGHT-1)
        
        if x_clipped != new_x : 
            # si on sort de la grille on rebondit en inversant la direction 
            self.direction = np.pi - self.direction # on choisit une nouvelle direction aleatoire pour eviter de rester coincé au bord
        if y_clipped != new_y : 
            self.direction = -self.direction

        old_x, old_y = self.x, self.y
    
        self.x = x_clipped 
        self.y = y_clipped 

        self.pheromone_deposit *= DECAY_FACTOR_STEP
        if self.pheromone_deposit < 0.001 : 
            self.pheromone_deposit = 0 

        return old_x, old_y

    
    def get_antenna_pos(self) :   
        # the head 
        hx = self.x + HALF_LENGTH_BODY*np.cos(self.direction)
        hy = self.y + HALF_LENGTH_BODY* np.sin(self.direction)

        left = (hx + self.length_antenna*np.cos(self.direction + self.angle_antenna), 
                hy + self.length_antenna*np.sin(self.direction + self.angle_antenna))
        
        right = (hx + self.length_antenna*np.cos(self.direction - self.angle_antenna), 
                 hy + self.length_antenna*np.sin(self.direction - self.angle_antenna))
        
        front = (hx + self.length_antenna*np.cos(self.direction), 
                 hy + self.length_antenna*np.sin(self.direction))
        

        return left, right, front
    def is_at_nest(self, nest) :
        x_nest, y_nest = nest.get_x_y()
        return (self.x - x_nest)**2 + (self.y - y_nest)**2 <= NEST_RADIUS**2 

    def interact(self, source, at_nest) :
        if source is not None and self.food_carried < MAX_FOOD_CARRIED : 
            # on ramasse de la nourriture si on en trouve et qu'on peut en porter plus 
            want_to_collect = min(FOOD_COLLECT_AMOUNT, MAX_FOOD_CARRIED - self.food_carried)
            taken = source.consume(want_to_collect)
            self.food_carried += taken
            if taken > 0 :
                self.eating_timer = EAT_DURATION # on doit attendre un peu avant de pouvoir bouger ou interagir à nouveau 

        elif self.food_carried > 0 and at_nest :
            deposited = self.food_carried
            self.food_carried = 0 
            self.nest_timer = NEST_DURATION # on doit attendre un peu avant de pouvoir bouger ou interagir à nouveau
            return deposited 
        return 0.0
    
    

        

 


