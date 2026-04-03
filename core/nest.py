from config import * 


class Nest: 

    def __init__(self, x, y) :
        if x < NEST_RADIUS or x >= GRID_WIDTH - NEST_RADIUS or y < NEST_RADIUS or y >= GRID_HEIGHT - NEST_RADIUS : 
            raise ValueError(f"Position ({x}, {y}) hors des limites de la grille ou trop proche du bord pour le nid")
        self.x = x 
        self.y = y 
        self.food_collected = 0 

    def get_x_y(self) :
        return self.x, self.y   