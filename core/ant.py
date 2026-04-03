from config import *
import numpy as np

class Ant : 

    def __init__(self, x, y, angle_antenna, length_antenna ) :

        self.x = x
        self.y = y 
        self.has_food = False 
        self.direction = np.random.uniform(0, 2*np.pi) # direction initiale aleatoire
        self.angle_antenna = angle_antenna
        self.length_antenna = length_antenna  # longueur de l'antenne en cases

    def move(self,delta_theta) : 
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

        old_x, old_y = int(self.x), int(self.y)
    
        self.x = x_clipped 
        self.y = y_clipped 

        return old_x, old_y

    
    def get_antenna_pos(self) : 
        return [(self.x + self.length_antenna*np.cos(self.direction + self.angle_antenna), self.y + self.length_antenna*np.sin(self.direction + self.angle_antenna)), (self.x + self.length_antenna*np.cos(self.direction - self.angle_antenna), self.y + self.length_antenna*np.sin(self.direction - self.angle_antenna))] 

    def is_at_nest(self, nest) :
        x_nest, y_nest = nest.get_x_y()
        return (self.x - x_nest)**2 + (self.y - y_nest)**2 <= NEST_RADIUS**2 

    def interact(self, source, at_nest) :
        if (not self.has_food) and source is not None and source.quantity > 0 :
            self.has_food = True 
            source.consume(1) # on prend ici 1 unité de nouriture 

        elif self.has_food and at_nest :
            self.has_food = False 
            return True 
        return False 
    
    

        

 


