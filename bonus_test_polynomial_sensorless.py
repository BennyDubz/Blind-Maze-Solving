from Maze import Maze

from uninformed_search import bfs_search
from bonus_polynomial_sensorless_problem import SensorlessPolynomial

# Author: Ben Williams '25
# Date: September 25th, 2023

print("Testing simple maze:")
test_simple_maze = Maze("./mazes/small_maze.maz")
test_sp_simple = SensorlessPolynomial(test_simple_maze)
result, move_list_simple = test_sp_simple.solve()
print(result)

print("Testing cm1:")
test_empty_maze = Maze("./mazes/custom_maze1.maz")
test_sp_empty = SensorlessPolynomial(test_empty_maze)
result, move_list_empty = test_sp_empty.solve()
print(result)

print("Testing cm2:")
test_empty_maze = Maze("./mazes/custom_maze2.maz")
test_sp_empty = SensorlessPolynomial(test_empty_maze)
result, move_list_cm2 = test_sp_empty.solve()
print(result)

# This maze really struggled with the astar search!
print("Testing cm3:")
test_x_maze = Maze("./mazes/custom_maze3.maz")
test_sp_x = SensorlessPolynomial(test_x_maze)
result, move_list_cm3 = test_sp_x.solve()
print(result)

###################################################
# I recommend uncommenting this animate_path call!
###################################################
# test_sp_x.animate_path(result.path, move_list_cm3)

# # An even bigger version of the x maze
print("Testing cm4:")
test_many_x_maze = Maze("./mazes/custom_maze4.maz")
test_sp_many_x = SensorlessPolynomial(test_many_x_maze)
result, move_list_many_x = test_sp_many_x.solve()
print(result)

print("Testing random_maze:")
# Test large 40x40 random maze
test_big_maze = Maze("./mazes/random_maze1.maz")
test_sp_big_rand = SensorlessPolynomial(test_big_maze)
result, move_list_big_rand = test_sp_big_rand.solve()
print(result)







