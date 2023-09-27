from Maze import Maze
from time import sleep

# Author: Ben Williams '25
# Date: September 22nd, 2023


# A version of Maze world where the robot is blind and has no idea where it starts
class SensorlessProblem:
    def __init__(self, maze):
        self.maze = maze
        # The robot could be anywhere - so we start with all the floor spaces
        self.start_state = self.get_open_spaces()

        # Goal state in this case is how many possibilities we want to have left
        self.goal_state = 1

    def get_successors(self, state):
        successor_states = []

        # Loop through each possible action, except this time we do not allow waiting
        for x_mov in range(-1, 2):
            for y_mov in range(-1, 2):
                # Ignore diagonal moves
                if abs(x_mov) + abs(y_mov) > 1:
                    continue

                # Do not allow waiting
                if x_mov == y_mov == 0:
                    continue

                new_state = set()
                # Try the movement on all current possible locations
                for possible_location in state:
                    new_x = possible_location[0] + x_mov
                    new_y = possible_location[1] + y_mov

                    # If the floor is open from this possible location, we could end up there
                    if self.maze.is_floor(new_x, new_y):
                        new_state.add((new_x, new_y))
                    # Otherwise, we hit a wall and stay in the same spot
                    else:
                        new_state.add(possible_location)

                successor_states.append(tuple(new_state))

        return successor_states

    def __str__(self):
        string = "Blind robot problem: "
        return string

    # In this, the letters represent all possible locations the single robot could be in
    #   We animate the narrowing-down of positions over time
    def animate_path(self, path):
        # Convert the start state into a list of locations
        start_list_of_tuples = list(self.start_state)
        start_possible_positions = []
        for possible_position in start_list_of_tuples:
            start_possible_positions.extend(list(possible_position))

        # Reset locations in the maze
        self.maze.robotloc = start_possible_positions

        for state in path:
            print(str(self))

            # Convert the state into a list of locations
            list_of_tuples = list(state)
            robot_possible_positions = []
            for possible_position in list_of_tuples:
                robot_possible_positions.extend(list(possible_position))
            self.maze.robotloc = robot_possible_positions

            sleep(1)
            print(str(self.maze))

    # Returns a list of all floor locations on the maze
    def get_open_spaces(self):
        open_spaces = []
        # Find every floor location on the maze
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if self.maze.is_floor(x, y):
                    open_spaces.append((x, y))
        return tuple(open_spaces)

    # If there is only one possible location, then we know where we are and the problem is solved
    def is_goal_state(self, state):
        return len(state) == 1

    # So that we can run the BFS on this
    def is_safe_state(self, state):
        return True


## A bit of test code
if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)
