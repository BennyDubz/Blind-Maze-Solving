from random import random

# Author: Ben Williams '25
# Date: September 25th, 2023
# Simple maze generator. Not guaranteed to have only one connected component, though.
width = 40
height = 40
wall_chance = 0.1

f = open("mazes/random_maze1.maz", "w")

for col in range(width):
    for row in range(height):
        if random() < wall_chance:
            f.write("#")
        else:
            f.write(".")
    f.write("\n")

f.close()
