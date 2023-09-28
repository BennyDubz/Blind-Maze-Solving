# Maze Solving

#### Ben Williams - September 27th, 2023

This project is the implementation of several maze solving algorithms in different situations. The mazes are 2D, and examples can be seen in the /mazes folder, where . is an open/floor space, and # is a wall. The robots in these mazes can move 1 space north, south, east, or west per move.

While most of this was originally assigned as an assignment in the class COSC 76 - Artificial Intelligence at Dartmouth, the polynomial solution was extra and is the most impressive part of this project.

## Problem Descriptions

### Mazeworld

In Mazeworld, we have multiple different robots in different locations in the maze. They know where they are, and they each have individual goal locations in the maze that they wish to get to.

The challenge is how to get each robot to its goal location while using the least amount of fuel (waiting uses no fuel). These robots cannot be on the same space as each other, so they may have to coordinate.

The solution involves using an Astar graph search algorithm with the Manhattan heuristic. More information can be seen in the code and in the documentation.

### Sensorless Mazeworld

In this problem, we have a robot that gets placed somewhere in the maze - but its sensors are broken/missing. It still has a compass, so it can still go north, east, south, or west on command. However, it has no idea where it is in the maze, and cannot even tell if it runs into a wall. How can this robot find out where it is?

This problem involves a large belief state first involving every open space on the maze, and finding a set of moves that eventually ensures that the robot knows exactly where it is. From there, it is trivial to find the path from that known-spot to the goal. The implementation and testing details can be found in the code and in the documentation.

### Sensorless Mazeworld Polynomial Solution

This is the same problem as previous one, but note that the number of possibilities of the belief space starts at 2^(num_floor_spaces), which is extremely large. A normal graph search algorithm on the problem cannot handle even moderately sized mazes as the belief space is too large.

Therefore, we needed to find a way to solve the Sensorless robot problem in polynomial time, rather than exponential time. It involves repeated graph searches on a smaller scale that systematically reduce the size of the belief space over time. Again, implementation details and additional information can be found in the documentation and in the code.


