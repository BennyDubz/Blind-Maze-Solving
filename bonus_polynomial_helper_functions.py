from collections import deque
from SearchSolution import SearchSolution
from Maze import Maze
from MazeworldProblem import MazeworldProblem

# Author: Ben Williams '25
# Date: September 24th-25th, 2023

# Uses bidirectional BFS to find a path between the start and end states
# Implemented without a wrapper node
def bi_directional_bfs(search_problem, start_state, end_state):
    # Initialize solution
    solution = SearchSolution(search_problem, "Bi-Directional BFS")

    # Initialize visited dictionaries and backtracking dictionaries
    visited_from_forward = dict()
    visited_from_backward = dict()
    visited_from_forward[start_state] = None
    visited_from_backward[end_state] = None

    # two queues - one for each position
    forward_queue = deque()
    forward_queue.appendleft(start_state)
    backward_queue = deque()
    backward_queue.appendleft(end_state)

    # Run until either is empty (would mean there is not a path between the two locations)
    while len(forward_queue) > 0 and len(backward_queue) > 0:
        forward_state = forward_queue.pop()
        backward_state = backward_queue.pop()

        solution.nodes_visited += 2

        # If we have seen either of these locations before, we are done
        if forward_state in visited_from_backward.keys():
            solution.path = bi_directional_backchain(forward_state, visited_from_forward, visited_from_backward)
            return solution

        if backward_state in visited_from_forward.keys():
            solution.path = bi_directional_backchain(backward_state, visited_from_forward, visited_from_backward)
            return solution

        forward_successors = search_problem.get_successors(forward_state)
        backward_successors = search_problem.get_successors(backward_state)

        # Add forward successors to queue
        for successor in forward_successors:
            if successor not in visited_from_forward.keys():
                visited_from_forward[successor] = forward_state
                forward_queue.appendleft(successor)

        # Add backward successors to queue
        for successor in backward_successors:
            if successor not in visited_from_backward.keys():
                visited_from_backward[successor] = backward_state
                backward_queue.appendleft(successor)

    return solution


# Finds the path from the beginning to the end node from the bi_directional_bfs
def bi_directional_backchain(middle_state, visited_from_forward, visited_from_backward):
    forward_path = []
    backward_path = []

    # Build the forward path
    forward_node = middle_state
    while forward_node:
        forward_path.append(forward_node)
        forward_node = visited_from_forward[forward_node]

    # Reverse the path so that it goes forward
    forward_path.reverse()

    # Remove the middle_state from this so that there are no duplicates
    forward_path.remove(middle_state)

    # Build the backward path
    backward_node = middle_state
    while backward_node:
        backward_path.append(backward_node)
        backward_node = visited_from_backward[backward_node]

    # Backward path does not need to be reversed (as we want it in the reverse order as that goes forwards)
    forward_path.extend(backward_path)
    return forward_path


# Given a path between two nodes, return the moves necessary to make in order to follow the path
# Specific to the maze problem, and is only for a single robot
# Moves are in the format: (0, 1) - North, (1, 0) - East, (0, -1) - South, (-1, 0) - West
def get_moves_from_path(path):
    moves = []
    for i in range(len(path) - 1):
        # Check for east
        if path[i][0] + 1 == path[i + 1][0]:
            moves.append((1, 0))
            continue

        # Check for north
        if path[i][1] + 1 == path[i+1][1]:
            moves.append((0, 1))
            continue

        # Check for west
        if path[i][0] - 1 == path[i + 1][0]:
            moves.append((-1, 0))
            continue

        # Check for south
        if path[i][1] - 1 == path[i + 1][1]:
            moves.append((0, -1))
            continue

    return moves


if __name__ == "__main__":
    maze = Maze("./mazes/random_maze1.maz")
    problem = MazeworldProblem(maze, (4, 33, 0))
    solution = bi_directional_bfs(problem, problem.start_state)
    print(solution.path)
    print(get_moves_from_path(solution.path))
