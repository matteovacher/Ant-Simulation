from config import *

class FoodSource:

    def __init__(self, type_food, x, y, quantity, recharge_rate=0.0):
        self.type_food = type_food
        self.x = x
        self.y = y
        self.quantity = quantity
        self.max_quantity = quantity
        self.recharge_rate = recharge_rate  # cases/pas de temps, 0 = pas de recharge

    def recharge(self):
        self.quantity = min(self.quantity + self.recharge_rate, self.max_quantity)

    def consume(self, amount):
        taken = min(self.quantity, amount)
        self.quantity -= taken
        return taken  # retourne ce qui a vraiment ete pris pas plus 
