from config import *

class FoodSource:

    APHID = 0 
    SUGAR = 1

    def __init__(self, type_food, x, y, quantity, recharge_rate):
        self.type_food = type_food
        self.x = x
        self.y = y
        if quantity >= 0 and quantity <= 1:
            self.quantity = quantity
            self.max_quantity = 1
        else : 
            raise ValueError("Quantity must be between 0 and 1")
        self.recharge_rate = recharge_rate  # cases/pas de temps, 0 = pas de recharge

    def recharge(self):
        self.quantity = min(self.quantity + self.recharge_rate, self.max_quantity)

    def consume(self, amount):
        taken = min(self.quantity, amount)
        self.quantity -= taken
        return taken  # retourne ce qui a vraiment ete pris pas plus

    def distance(self, x, y) : 
        return ((self.x - x)**2 + (self.y - y)**2)**0.5
