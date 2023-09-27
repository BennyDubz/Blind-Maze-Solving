from collections import deque
from SearchSolution import SearchSolution

# Author: Ben Williams '25
# Date: September 14th, 2023

# A node that wraps a state, and its parent node along the path
# Used for search problems
class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent


# Handles the back-chaining after a search has been performed
# Input: The final SearchNode on a path to the goal state
# Output: The path from the start state to the goal state as an array of states
def backchain(final_node):
    path = []
    current_node = final_node
    while current_node is not None:
        path.append(current_node.state)
        current_node = current_node.parent

    # This ensures the start of the list is the starting state
    path.reverse()
    return path


# An implementation of breadth first search
# Input: search_problem - that has a start state, goal state, and a successor function
# Output: A SearchSolution object that contains the path to the goal state (if it exists)
def bfs_search(search_problem):
    # Instantiate data structures
    queue = deque()
    seen_already = set()
    start_node = SearchNode(search_problem.start_state)
    queue.append(start_node)
    solution = SearchSolution(search_problem, "BFS")

    # If in an illegal start state, do not search
    if not search_problem.is_safe_state(start_node.state):
        return solution

    # Base case for if there is no solution
    while len(queue) > 0:
        current_node = queue.pop()
        solution.nodes_visited += 1

        # Base case for if goal state has been reached
        if search_problem.is_goal_state(current_node.state):
            solution.path = backchain(current_node)
            break

        successor_states = search_problem.get_successors(current_node.state)
        new_states = []
        # Don't visit already-seen states
        for state in successor_states:
            if state not in seen_already:
                # Add new state to the end of the queue
                queue.appendleft(SearchNode(state, current_node))
                seen_already.add(state)
                new_states.append(state)

    return solution


# An implementation of depth first search
# Input: search_problem - that has a start state, goal state, and a successor function
# Input: depth_limit - the maximum depth at which the dfs will search
# Output: A SearchSolution object that contains the path to the goal state (if it exists)
def dfs_search(search_problem, depth_limit=100, node=None, solution=None, current_path_set=None):
    # if no node object given, create a new search from starting state
    if node is None:
        node = SearchNode(search_problem.start_state)
        current_path_set = set()
        current_path_set.add(node.state)
        if solution is None:
            solution = SearchSolution(search_problem, "DFS")

        # If in an illegal start state, do not search
        if not search_problem.is_safe_state(node.state):
            return solution

    # Increment the nodes visited
    solution.nodes_visited += 1

    # Base case for if this node is the goal
    if search_problem.is_goal_state(node.state):
        solution.path = backchain(node)
        return solution

    # Base case for depth limit
    if len(current_path_set) >= depth_limit:
        return solution

    # Only DFS on nodes not on current path
    successor_states = search_problem.get_successors(node.state)
    for state in successor_states:
        if state not in current_path_set:
            # Create a new node for the new state
            new_node = SearchNode(state, node)

            # Continue searching
            current_path_set.add(state)
            solution = dfs_search(search_problem, depth_limit, new_node, solution, current_path_set)

            # If the final path has been found, break out early
            if solution.path:
                return solution

            # Remove this state from the current_path_set as the solution has not been found
            current_path_set.remove(state)

    return solution


# An implementation of an iterative deepening search
# Input: search_problem - that has a start state, goal state, and a successor function
# Input: depth_limit - the maximum depth at which the IDS will no longer continue
# Output: A SearchSolution object that contains the path to the goal state (if it exists)
def ids_search(search_problem, depth_limit=100):
    curr_max_depth = 0
    solution = SearchSolution(search_problem, "IDS")

    # If in an illegal start state, do not search
    if not search_problem.is_safe_state(search_problem.start_state):
        return solution

    # Only search while under the depth limit, or until a solution has a path
    while curr_max_depth <= depth_limit and not solution.path:
        solution = dfs_search(search_problem, depth_limit=curr_max_depth, solution=solution)
        curr_max_depth += 1

    return solution
