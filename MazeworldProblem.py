from Maze import Maze
from time import sleep

# Author: Ben Williams '25
# Date: September 14th, 2023


class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.start_state = tuple(maze.robotloc)
        self.goal_state = goal_locations
        # Excludes final index that may represent whose turn it is
        self.num_robots = len(maze.robotloc) // 2

    def __str__(self):
        string = "Mazeworld problem: "
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[0:(len(self.start_state) - 1)])
        print("Start state: ", self.start_state)
        print("Goal state: ", self.goal_state)
        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[0:(len(self.start_state) - 1)])
            sleep(1)

            print(str(self.maze))

    # Move robots together or separately?
    def get_successors(self, state):
        # Update locations on the maze
        self.maze.robotloc = list(state)
        successor_states = []

        # Determine which robot is being moved
        robot_id = state[len(state) - 1]

        # Go through all possible movements
        for x_mov in range(-1, 2):
            for y_mov in range(-1, 2):
                # Ignore diagonal moves
                if abs(x_mov) + abs(y_mov) > 1:
                    continue
                new_state = []
                new_state.extend(state)
                new_state[robot_id * 2] += x_mov
                new_state[1 + robot_id * 2] += y_mov
                new_state[len(new_state) - 1] = (robot_id + 1) % self.num_robots
                if self.is_free_space(new_state[robot_id * 2], new_state[1 + robot_id * 2]) or (x_mov == 0 and y_mov == 0):
                    successor_states.append(tuple(new_state))

        return successor_states

    # Returns whether a space is free and open on the current maze
    def is_free_space(self, x, y):
        if self.maze.is_floor(x, y) and not self.maze.has_robot(x, y):
            return True
        return False

    # Returns whether all the robots are at the goal positions or not
    def is_goal_state(self, state):
        self.maze.robotloc = list(state)
        # We ignore the turn-element index of the state
        for i in range(len(state) - 1):
            if state[i] != self.goal_state[i]:
                return False
        return True


# A bit of test code. You might want to add to it to verify that things
#  work as expected.
if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
    print(test_mp.maze)
    # print(test_mp.get_successors((1, 0, 1, 1, 2, 1, 0)))
    # print(test_mp.get_successors((1, 0, 1, 1, 2, 1, 1)))
    # print(test_mp.get_successors((1, 0, 1, 1, 2, 1, 2)))

    print(test_mp.get_successors((1, 0, 3, 1, 2, 5, 0)))
    # print(test_mp.is_free_space(1, 1))
