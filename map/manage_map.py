import json 
import os

from matplotlib.pylab import number
from core.food_grid import FoodGrid
from core.food_source import FoodSource
from core.nest import Nest

def ask_map() : 
    number = input("\n Enter the map number here : ")
    return number

def map_rules() : 
    print("\n --- HOW TO CHOSE A MAP --- \n")
    print(" - The map will be chosen in the map/stock folder, go check if some map are interesting there, if not create your own with the create_map.py script")
    print(" - You will be asked a question, answer it :) \n")
    print(" --- END --- \n")

def load_map() : 
    base_dir = os.path.dirname(os.path.abspath(__file__))
    stock_dir = os.path.join(base_dir, "stock")
    map_rules()
    number = ask_map()
    with open(os.path.join(stock_dir, f"map_{number}.json")) as f:
        data = json.load(f)
    sources = [FoodSource(source["type_food"], source["x"], source["y"], source["quantity"], source["recharge_rate"]) for source in data["food_sources"]]
    nest = Nest(data["nest"]["x"], data["nest"]["y"])
    return FoodGrid(sources), nest