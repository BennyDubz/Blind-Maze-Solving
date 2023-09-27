from MazeworldProblem import MazeworldProblem
from Maze import Maze

from uninformed_search import bfs_search
from astar_search import astar_search


# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state, goal_state):
    return 0


# Returns the sum of the manhattan distances between each robot and their goal
def manhattan_heuristic(state, goal_state):
    difference = 0
    # Find all differences in location, and add them up
    for location in range(len(state) - 1):
        difference += abs(state[location] - goal_state[location])

    return difference


# Compares the current state and the next state to see if fuel is used
def robot_fuel_cost(current_state, next_state):
    # We ignore only the final index that says which robot's turn it is
    if current_state[0:(len(current_state) - 1)] != next_state[0:(len(next_state) - 1)]:
        return 1
    return 0


# Test problems
test_maze3 = Maze("./mazes/maze3.maz")
test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

# print(test_mp.get_successors(test_mp.start_state))

# this should explore a lot of nodes; it's just uniform-cost search
# print("Maze 3 with null-heuristic:")
# result = astar_search(test_mp, null_heuristic, robot_fuel_cost)
# print(result)
#
# # this should do a bit better:
# print("Maze 3 with Manhattan Heuristic:")
# result = astar_search(test_mp, manhattan_heuristic, robot_fuel_cost)
# print(result)
# # test_mp.animate_path(result.path)
#
# # Your additional tests here:
#
# # Note that the Manhattan heuristic might struggle here!
# print("Robot Coordination Maze w/ Manhattan Heuristic:")
# test_maze_coordination = Maze("./mazes/robot_coordination.maz")
# test_mp_mc = MazeworldProblem(test_maze_coordination, (8, 0, 7, 0, 6, 0))
# result = astar_search(test_mp_mc, manhattan_heuristic, robot_fuel_cost)
# print(result)
#
# print("Robot Coordination Maze w/ Null Heuristic:")
# result = astar_search(test_mp_mc, null_heuristic, robot_fuel_cost)
# print(result)

print("8-Puzzle with manhattan heuristic")
test_8_puzzle = Maze("./mazes/8_puzzle.maz")
test_mp_8p = MazeworldProblem(test_8_puzzle, (0, 2, 1, 2, 2, 2, 0, 1, 1, 1, 2, 1, 0, 0, 1, 0))
result = astar_search(test_mp_8p, manhattan_heuristic, robot_fuel_cost)
print(result)
test_mp_8p.animate_path(result.path)

print("8-Puzzle with null heuristic")
test_8_puzzle = Maze("./mazes/8_puzzle.maz")
test_mp_8p = MazeworldProblem(test_8_puzzle, (0, 2, 1, 2, 2, 2, 0, 1, 1, 1, 2, 1, 0, 0, 1, 0))
result = astar_search(test_mp_8p, null_heuristic, robot_fuel_cost)
print(result)

# result = astar_search(test_mp_mc, null_heuristic, robot_fuel_cost)
# print(result)


