from MazeSolverV2 import *

# For organization purposes, we'll run the functions here :)

# NOTE: The algorithms works for any maze whether it's square or non-square

'''
To understand the path computed: U = Up , D = Down , L = Left , R = Right
To see the maze being solved, uncomment the render part in the BFS, DFS, Greedy, and/or A-Star algorithms.
'''

# Maze 1
print("\n------- Maze 1 -------\n")
filename = "maze1.txt"
maze = create_data(filename)
BFS_Maze_Solver(maze, filename)
print("----\n")
DFS_Maze_Solver(maze, filename)
print("----\n")
Greedy_Maze_Solver(maze, filename)
print("----\n")
AStar_Maze_Solver(maze, filename)

# Maze 2
print("------- Maze 2 -------\n")
filename = "maze2.txt"
maze = create_data(filename)
BFS_Maze_Solver(maze, filename)
print("----\n")
DFS_Maze_Solver(maze, filename)
print("----\n")
Greedy_Maze_Solver(maze, filename)
print("----\n")
AStar_Maze_Solver(maze, filename)

# Maze 3
print("------- Maze 3 -------\n")
filename = "maze3.txt"
maze = create_data(filename)
BFS_Maze_Solver(maze, filename)
print("----\n")
DFS_Maze_Solver(maze, filename)
print("----\n")
Greedy_Maze_Solver(maze, filename)
print("----\n")
AStar_Maze_Solver(maze, filename)

# Maze 4
print("------- Maze 4 -------\n")
filename = "maze4.txt"
maze = create_data(filename)
BFS_Maze_Solver(maze, filename)
print("----\n")
DFS_Maze_Solver(maze, filename)
print("----\n")
Greedy_Maze_Solver(maze, filename)
print("----\n")
AStar_Maze_Solver(maze, filename)