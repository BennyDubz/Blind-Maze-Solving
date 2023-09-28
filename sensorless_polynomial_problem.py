from sensorless_polynomial_helper_functions import *
from Maze import Maze
from time import sleep
from random import randint
# Author: Ben Williams '25
# Date: September 24th-25th, 2023


# A version of Maze world where the robot is blind and has no idea where it starts
class SensorlessPolynomial:
    def __init__(self, maze):
        self.maze = maze
        # The robot could be anywhere - so we start with all the floor spaces
        self.start_state = self.get_open_spaces()

        # The length of the state that we are looking for
        self.goal_state = 1

    def solve(self):
        # Nodes visited is not quite as applicable, but we count that through the BD-BFS
        solution = SearchSolution(self, "Single-Possibility Removal through repeated BiDirectional BFS")
        path = []
        move_path = []

        next_state_info = self.get_next_state(self.start_state, solution)

        # Continue until the belief state only has one state
        while len(next_state_info[0]) > 1:
            path.extend(next_state_info[1])
            move_path.extend(next_state_info[2])
            next_state_info = self.get_next_state(next_state_info[0], solution)

        # Invalid maze (> 1 connected component), no solution
        if not next_state_info[0]:
            solution.path = []
            return solution, []

        # To get the final moves
        path.extend(next_state_info[1])
        move_path.extend(next_state_info[2])

        solution.path = path
        return solution, move_path

    # Returns the next state, the moves that were required to get there,
    #   and the path of belief states along the way
    def get_next_state(self, state, solution):
        belief_state_path = [state]
        move_path = []

        # This is the goal state
        if len(state) == 1:
            return state

        new_state = state

        # We could pick the first and last state out of convenience, but random actually works better.
        # location_1 = new_state[0]
        # location_2 = new_state[len(state) - 1]
        rand_index_1 = randint(0, len(new_state) - 1)
        rand_index_2 = randint(0, len(new_state) - 1)
        while rand_index_2 == rand_index_1:
            rand_index_2 = randint(0, len(new_state) - 1)

        location_1 = new_state[rand_index_1]
        location_2 = new_state[rand_index_2]

        search_loc1_loc2_solution = bi_directional_bfs(self, location_1, location_2)

        # Impossible - Non connected components
        if not search_loc1_loc2_solution.path:
            return [], [], []

        solution.nodes_visited += search_loc1_loc2_solution.nodes_visited
        moves = get_moves_from_path(search_loc1_loc2_solution.path)
        move_path.extend(moves)

        # Then, we get the successors to the belief state
        #   But we keep track of if location_1 and location_2 end up in the same spot, otherwise we bfs and move again
        while location_1 != location_2:
            # Get the next belief state after a series of moves, along with the path travelled
            result = self.move_belief_state(new_state, location_1, location_2, moves)
            location_1 = result[0]
            location_2 = result[1]
            path_addition = result[2]
            new_state = path_addition[len(path_addition) - 1]

            # Remove final element - prevents duplicate in the path (since end of last path is start of new one)
            belief_state_path.remove(belief_state_path[len(belief_state_path) - 1])
            belief_state_path.extend(path_addition)

            # Then get the new (shorter!) path and move set, and go again
            if location_1 != location_2:
                search_loc1_loc2_solution = bi_directional_bfs(self, location_1, location_2)
                solution.nodes_visited += search_loc1_loc2_solution.nodes_visited
                moves = get_moves_from_path(search_loc1_loc2_solution.path)
                move_path.extend(moves)

        # Could add total moves... might be cool when visualizing it
        return new_state, belief_state_path, move_path

    # Used to get the successors from a single location
    #   ##################################
    #   Not to be used in a normal search on the entire SensorlessPolynomial!
    #   This is used so that we can perform searches between two locations on the maze within
    #      the scope of just this problem.
    #   ##################################
    def get_successors(self, location):
        successor_states = []
        for x_mov in range(-1, 2):
            for y_mov in range(-1, 2):
                # No diagonal moves
                if abs(x_mov) + abs(y_mov) > 1:
                    continue

                # No waiting
                if x_mov == y_mov == 0:
                    continue

                # If it is a floor space, it is a successor
                if self.maze.is_floor(location[0] + x_mov, location[1] + y_mov):
                    successor_states.append((location[0] + x_mov, location[1] + y_mov))

        return successor_states

    # Modifies the belief state, location_1, location_2 to adjust to the set of moves given
    # Also returns the path of belief states reached along the way
    def move_belief_state(self, state, location_1, location_2, moves):
        path = []
        for move in moves:
            # Add the current state to the path
            path.append(state)

            # First adjust location_1 and location_2
            if self.maze.is_floor(location_1[0] + move[0], location_1[1] + move[1]):
                # If the move leads to a floor space, go there
                location_1 = (location_1[0] + move[0], location_1[1] + move[1])

            if self.maze.is_floor(location_2[0] + move[0], location_2[1] + move[1]):
                # If the move leads to a floor space, go there
                location_2 = (location_2[0] + move[0], location_2[1] + move[1])

            # Then adjust the whole belief state
            new_state = set()
            for possible_location in state:
                new_x = possible_location[0] + move[0]
                new_y = possible_location[1] + move[1]
                if self.maze.is_floor(new_x, new_y):
                    new_state.add((new_x, new_y))
                else:
                    new_state.add(possible_location)

            state = tuple(new_state)

        # Append the final state
        path.append(state)

        return location_1, location_2, path

    def __str__(self):
        string = "Polynomial Time Blind Robot Problem: "
        return string

    # In this, the letters represent all possible locations the single robot could be in
    #   We animate the narrowing-down of positions over time
    def animate_path(self, path, move_list=None):
        move_dict = dict()
        move_dict[(1, 0)] = "East"
        move_dict[(0, 1)] = "North"
        move_dict[(-1, 0)] = "West"
        move_dict[(0, -1)] = "South"

        # Convert the start state into a list of locations
        start_list_of_tuples = list(self.start_state)
        start_possible_positions = []
        for possible_position in start_list_of_tuples:
            start_possible_positions.extend(list(possible_position))

        # Reset locations in the maze
        self.maze.robotloc = start_possible_positions
        index = -1
        for state in path:
            print(str(self))

            # Convert the state into a list of locations
            list_of_tuples = list(state)
            robot_possible_positions = []
            for possible_position in list_of_tuples:
                robot_possible_positions.extend(list(possible_position))
            self.maze.robotloc = robot_possible_positions

            sleep(1)
            if move_list:
                if len(move_list) > index >= 0:
                    print("Next Move: ", move_dict[move_list[index]])
                index += 1
            print(str(self.maze))

    def get_open_spaces(self):
        open_spaces = []
        # Find every floor location on the maze
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if self.maze.is_floor(x, y):
                    open_spaces.append((x, y))
        return tuple(open_spaces)

    # Returns if the given state is equal to the psuedo goal state
    def is_goal_state(self, state):
        return len(state) == self.goal_state


## A bit of test code
if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    # test_problem = (test_maze3)
