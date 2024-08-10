import random
import pandas as pd
import numpy as np

def monty_hall_simulation(doors=[]):
    # Doors 1 --> Brand New Car! :D , 0 --> Goat :') 
    # ls = [0,1,0]
    ls = doors

    current_selection = random.choice(ls)
    # Remove the door already selected by the student
    ls.remove(current_selection)

    # Remove the door that contains goal for sure
    ls.remove(min(ls))

    # what if the student select the raiming door
    new_selection = ls[0]


    return current_selection,new_selection

current_selection_ls = list()
new_selection_ls = list()
for i in range(0,10000):
    current_selection,new_selection =monty_hall_simulation(doors = [0,1,0])
    current_selection_ls.append(current_selection)
    new_selection_ls.append(new_selection)

print("current_selection: ",(sum(current_selection_ls)/10000)*100,"\nnew_selection: ",(sum(new_selection_ls)/10000)*100)