from Maze import Maze

from uninformed_search import bfs_search
from astar_search import astar_search
from SensorlessProblem import SensorlessProblem

# Author: Ben Williams '25
# Date: September 22nd, 2023


# A simple heuristic that just returns the total size of the state
#   ie: The total number of possible locations
def state_size_heuristic(state, goal_state=None):
    return len(state)


def null_heuristic(state, goal_state=None):
    return 0


print("Testing small maze")
test_simple_maze = Maze("./mazes/small_maze.maz")
test_sp_simple = SensorlessProblem(test_simple_maze)
result = astar_search(test_sp_simple, state_size_heuristic)
print(result)
# test_sp_simple.animate_path(result.path)

# result = astar_search(test_sp_simple, null_heuristic)
# print(result)

# print("Testing empty maze w/ state_size_heuristic:")
# test_empty_maze = Maze("./mazes/custom_maze1.maz")
# test_sp_empty = SensorlessProblem(test_empty_maze)
# result = astar_search(test_sp_empty, state_size_heuristic)
# print(result)
# print("Testing empty maze w/ null_heuristic:")
# result = astar_search(test_sp_empty, null_heuristic)
# print(result)
print("Testing cm1:")
test_harder_maze = Maze("./mazes/custom_maze1.maz")
test_sp_hm = SensorlessProblem(test_harder_maze)
result = astar_search(test_sp_hm, state_size_heuristic)
print(result)

print("Testing cm2:")
test_harder_maze = Maze("./mazes/custom_maze2.maz")
test_sp_hm = SensorlessProblem(test_harder_maze)
result = astar_search(test_sp_hm, state_size_heuristic)
print(result)

print("Testing cm3:")
test_harder_maze = Maze("./mazes/custom_maze3.maz")
test_sp_hm = SensorlessProblem(test_harder_maze)
result = astar_search(test_sp_hm, state_size_heuristic)
print(result)

print("Testing random:")
test_harder_maze = Maze("./mazes/random_maze1.maz")
test_sp_hm = SensorlessProblem(test_harder_maze)
result = astar_search(test_sp_hm, state_size_heuristic)
print(result)

# test_x_maze = Maze("./mazes/custom_maze3.maz")
# test_sp_x = SensorlessProblem(test_x_maze)
# result = astar_search(test_sp_x, state_size_heuristic)
# print(result)






