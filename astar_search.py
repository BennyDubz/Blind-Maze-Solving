from SearchSolution import SearchSolution
from heapq import heappush, heappop


class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        # Heuristic cost
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost

    def priority(self):
        # heuristic + actual cost
        return self.heuristic + self.transition_cost

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


# Performs an astar search on the search_problem, and returns a search_solution
# Parameter: heuristic_fn - The heuristic function to be used on states. heuristic_fn must take (state, goal_state)
#   as its parameters
# Parameter: cost_fn - A function for calculating the transition cost between two states. It is optional,
#   and if it is not provided the cost will be the length of the path so far by default. It takes both
#   the current_state and next_state as parameters.
def astar_search(search_problem, heuristic_fn, cost_fn=None):
    # To keep code concise
    goal_state = search_problem.goal_state

    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state, goal_state))
    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    # Will only have the visited cost, not including the heuristic
    visited_cost = dict()
    visited_cost[start_node.state] = 0

    # Base case for until every possibility has been searched
    while len(pqueue) > 0:
        current_node = heappop(pqueue)

        # Do not consider nodes that already have a better path to them than the current one
        if visited_cost[current_node.state] + heuristic_fn(current_node.state, goal_state) < current_node.priority():
            continue

        solution.nodes_visited += 1

        # If we are at the goal state, backchain and return the solution
        if search_problem.is_goal_state(current_node.state):
            solution.path = backchain(current_node)
            solution.cost = visited_cost[current_node.state]
            return solution

        successor_states = search_problem.get_successors(current_node.state)

        # The new visited cost of any the successor states
        for state in successor_states:
            if cost_fn:
                new_visited_cost = visited_cost[current_node.state] + cost_fn(current_node.state, state)
            else:
                new_visited_cost = visited_cost[current_node.state] + 1
            # If we have not seen it yet, then add the node to the pqueue
            if state not in visited_cost.keys():
                # Figure out the cost, wrap it into a node, and add it to the pqueue
                new_node = AstarNode(state, heuristic_fn(state, goal_state), current_node, new_visited_cost)
                # Find the cost between this node and the next
                visited_cost[state] = new_visited_cost
                heappush(pqueue, new_node)
            # If we have seen it, only add it if the cost is better
            else:
                if new_visited_cost < visited_cost[state]:
                    new_node = AstarNode(state, heuristic_fn(state, goal_state), current_node, new_visited_cost)
                    visited_cost[state] = new_visited_cost
                    heappush(pqueue, new_node)

    return solution
