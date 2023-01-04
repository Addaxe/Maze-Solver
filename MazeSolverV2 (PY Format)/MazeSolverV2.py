import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
from collections import deque
import numpy as np
import heapq

#------------------------------------- Helper Functions & Class -------------------------------------

# Function 1: Convert a maze TXT file to 2D array
def create_data(filename):
    maze = []
    with open(filename, "r") as file:
        for line in file:
            maze.append([float(s) for s in line if s != '\n'])
    return maze

# Function 2: Render the maze and return the fig, ax for animation
def render(maze, title): # Expects a 2D array of floats
    scale = 2 # Adjust this number if you want change the size of the rendered maze
    maze_width = len(maze[0])
    maze_height = len(maze)
    x = round(scale * (maze_width/10)) 
    y = round(scale * (maze_height/10)) 
    fig, ax = plt.subplots(figsize=(x,y))

    ax.clear()
    ax.pcolormesh(maze)
    plt.xticks([]); plt.yticks([])
    plt.title(title)
    return (fig, ax)

# Function 3: Implement the an algorithm to find the coordinates of "2" and "3"
def find_coordinates(maze, maze_width, find):
    '''
        Purpose: Using the 1D array, "maze", we must find the string, 
        "find" and return its coordinates in the 2D format.

        The coordinates will be used to compute the Manhattan distance, which is our h(n)
    '''

    # Process A: Convert 1D array to 2D array if param 'maze' is a 1D
    maze2D = []
    if np.array(maze).ndim == 1:
        maze_area = len(maze)
        a = 0; b = maze_width
        while b < maze_area + maze_width:
            maze2D.append([maze[i] for i in range(a,b)])
            a += maze_width; b += maze_width
        maze2D.reverse()
    else:
        maze2D = maze.copy()

    # Process B: Find coordinates in 2D array format
    x = -1; y = -1; maze_height = len(maze2D)
    for r in range(maze_height):
        if find in maze2D[r]:
            x = r; y = maze2D[r].index(find)
            break
    return (x, y)

# Class 1: Create the Node class
class Node:
    def __init__(self, p, a, s, d, c):
        self.parent = p
        self.action = a
        self.state = s
        self.depth = d
        self.cost = c

    def __lt__(self, other):
        return self.cost < other.cost

#------------------------------------- BFS Implementation -------------------------------------

'''
In the TXT files, please note the following:
    2 means the agent
    3 means goal node
'''

def BFS_Maze_Solver(maze, filename): # Input is a 2D array with floats created with create_data(...)
    maze_width = len(maze[0])
    flattened = [str(int(c)) for r in maze for c in r] # 2D to 1D array

    starter_node = Node(None, None, flattened, 0, None)
    queue = deque([starter_node])
    
    starter_node = "".join(flattened)
    maze_area = len(starter_node)
    visited = {starter_node}
    min = 0; max = len(starter_node) - 1
    while queue:
        queue_size = len(queue)
        for _ in range(queue_size):
            current_node = queue.popleft()
            current_state = current_node.state

            if '3' not in current_state:
                path = []
                states = []
                while current_node.parent != None: # We're backtracking to compute the path
                    path.append(current_node.action)

                    current_state = []
                    a = 0; b = maze_width
                    while b < maze_area + maze_width:
                        current_state.append([float(current_node.state[i]) for i in range(a,b)])
                        a += maze_width; b += maze_width

                    current_state.reverse()
                    states.append(current_state)
                    current_node = current_node.parent

                initial_maze = maze.copy(); initial_maze.reverse()
                states.append(initial_maze)
                states.reverse()

                prev = []
                for s in states:
                    if prev:
                        for x,y in prev:
                            s[x][y] = 3.0
                    prev.append(find_coordinates(s, maze_width, 2.0))
                
                maze_num = filename.split(".")[0]
                maze_num = maze_num[len(maze_num)-1]
                title = "Maze " + str(maze_num) + " Solved With BFS"
                fig, ax = render(states[0], title)

                def animate(i):
                    ax.clear()
                    ax.pcolormesh(states[i])
                    plt.xticks([]); plt.yticks([])
                    plt.title(title)

                # The animation has to be assigned to a variable to work
                animation = FuncAnimation(fig, animate, frames=len(states), interval=100, repeat=False)
                plt.show()

                path.reverse() # We reverse since we're backtracking
                print("[BFS] The maze has been solved with these " + str(len(path)) + " steps: " + str(path) + "\n")
                print("[BFS] The number of explored nodes is " + str(len(visited)) + ".\n")
                return path

            for action in ["U", "D", "L", "R"]:
                next_state = current_state.copy()
                curr_pos = next_state.index("2") # We're finding the current position of the start node (agent)

                if action == "U" and (min <= curr_pos - maze_width <= max) and next_state[curr_pos - maze_width] != '1': 
                    next_state[curr_pos] = '0'; next_state[curr_pos - maze_width] = '2'
                elif action == "D" and (min <= curr_pos + maze_width <= max) and next_state[curr_pos + maze_width] != '1': 
                    next_state[curr_pos] = '0'; next_state[curr_pos + maze_width] = '2'
                elif action == "L" and (min <= curr_pos - 1 <= max) and next_state[curr_pos - 1] != '1':
                    next_state[curr_pos] = '0'; next_state[curr_pos - 1] = '2'
                elif action == "R" and (min <= curr_pos + 1 <= max) and next_state[curr_pos + 1] != '1':
                    next_state[curr_pos] = '0'; next_state[curr_pos + 1] = '2'
                
                next_state = "".join(s for s in next_state) # We convert the 1D array to a string
                if next_state not in visited:
                    visited.add(next_state) # We add the string form of the new state to the set

                    next_state = [s for s in next_state]
                    # We create our child node - Node(parent, action, state, depth, cost)
                    queue.append(Node(current_node, action, next_state, current_node.depth + 1, None))

    print("The maze could not be solved!")
    return None 

#------------------------------------- DFS Implementation -------------------------------------

'''
In the TXT files, please note the following:
    2 means the agent
    3 means goal node
'''

def DFS_Maze_Solver(maze, filename): # Input is a 2D array with floats created with create_data(...)
    maze_width = len(maze[0])
    flattened = [str(int(c)) for r in maze for c in r] # 2D to 1D array

    starter_node = Node(None, None, flattened, 0, None)
    stack = [starter_node]
    
    starter_node = "".join(flattened)
    maze_area = len(starter_node)
    visited = {starter_node}
    min = 0; max = len(starter_node) - 1
    while stack:
        stack_size = len(stack)
        for _ in range(stack_size):
            current_node = stack.pop()
            current_state = current_node.state

            if '3' not in current_state:
                path = []
                states = []
                while current_node.parent != None: # We're backtracking to compute the path
                    path.append(current_node.action)

                    current_state = []
                    a = 0; b = maze_width
                    while b < maze_area + maze_width:
                        current_state.append([float(current_node.state[i]) for i in range(a,b)])
                        a += maze_width; b += maze_width

                    current_state.reverse()
                    states.append(current_state)
                    current_node = current_node.parent

                initial_maze = maze.copy(); initial_maze.reverse()
                states.append(initial_maze)
                states.reverse()

                prev = []
                for s in states:
                    if prev:
                        for x,y in prev:
                            s[x][y] = 3.0
                    prev.append(find_coordinates(s, maze_width, 2.0))
                
                # Uncomment Lines 98-108 to render animation
                maze_num = filename.split(".")[0]
                maze_num = maze_num[len(maze_num)-1]
                title = "Maze " + str(maze_num) + " Solved With DFS"
                fig, ax = render(states[0], title)

                def animate(i):
                    ax.clear()
                    ax.pcolormesh(states[i])
                    plt.xticks([]); plt.yticks([])
                    plt.title(title)

                # The animation has to be assigned to a variable to work
                animation = FuncAnimation(fig, animate, frames=len(states), interval=100, repeat=False)
                plt.show()

                path.reverse() # We reverse since we're backtracking
                print("[DFS] The maze has been solved with these " + str(len(path)) + " steps: " + str(path) + "\n")
                print("[DFS] The number of explored nodes is " + str(len(visited)) + ".\n")
                return path

            for action in ["U", "D", "L", "R"]:
                next_state = current_state.copy()
                curr_pos = next_state.index("2") # We're finding the current position of the start node (agent)

                if action == "U" and (min <= curr_pos - maze_width <= max) and next_state[curr_pos - maze_width] != '1': 
                    next_state[curr_pos] = '0'; next_state[curr_pos - maze_width] = '2'
                elif action == "D" and (min <= curr_pos + maze_width <= max) and next_state[curr_pos + maze_width] != '1': 
                    next_state[curr_pos] = '0'; next_state[curr_pos + maze_width] = '2'
                elif action == "L" and (min <= curr_pos - 1 <= max) and next_state[curr_pos - 1] != '1':
                    next_state[curr_pos] = '0'; next_state[curr_pos - 1] = '2'
                elif action == "R" and (min <= curr_pos + 1 <= max) and next_state[curr_pos + 1] != '1':
                    next_state[curr_pos] = '0'; next_state[curr_pos + 1] = '2'
                
                next_state = "".join(s for s in next_state) # We convert the 1D array to a string
                if next_state not in visited:
                    visited.add(next_state) # We add the string form of the new state to the set

                    next_state = [s for s in next_state]
                    # We create our child node - Node(parent, action, state, depth, cost)
                    stack.append(Node(current_node, action, next_state, current_node.depth + 1, None))

    print("The maze could not be solved!")
    return None 

#------------------------------------- Greedy Implementation -------------------------------------

'''
In the TXT files, please note the following:
    2 means the agent
    3 means goal node
'''

def Greedy_Maze_Solver(maze, filename): # Input is a 2D array with floats created with create_data(...)
    maze_width = len(maze[0])
    flattened = [str(int(c)) for r in maze for c in r] # 2D to 1D array

    starter_coords = find_coordinates(flattened, maze_width, "2")
    goal_coords = find_coordinates(flattened, maze_width, "3")
    h = abs(starter_coords[0] - goal_coords[0]) + abs(starter_coords[1] - goal_coords[1])

    '''
    Heuristic Used: f(n) = h(n)
    h(n) = The Manhattan distance of the current node to goal node (h) 
    '''

    starter_node = Node(None, None, flattened, 0, h) # f(n) = h(n) is our cost here
    heap_priority_queue = [starter_node]
    heapq.heapify(heap_priority_queue)
    
    starter_node = "".join(flattened)
    maze_area = len(starter_node)
    visited = {starter_node}
    min = 0; max = len(starter_node) - 1
    while heap_priority_queue:
        queue_size = len(heap_priority_queue)
        for _ in range(queue_size):
            current_node = heapq.heappop(heap_priority_queue)
            current_state = current_node.state

            if '3' not in current_state:
                path = []
                states = []
                while current_node.parent != None: # We're backtracking to compute the path
                    path.append(current_node.action)
                    
                    current_state = []
                    a = 0; b = maze_width
                    while b < maze_area + maze_width:
                        current_state.append([float(current_node.state[i]) for i in range(a,b)])
                        a += maze_width; b += maze_width

                    current_state.reverse()
                    states.append(current_state)
                    current_node = current_node.parent
                
                initial_maze = maze.copy(); initial_maze.reverse()
                states.append(initial_maze)
                states.reverse()

                prev = []
                for s in states:
                    if prev:
                        for x,y in prev:
                            s[x][y] = 3.0
                    prev.append(find_coordinates(s, maze_width, 2.0))
                
                # Uncomment Lines 234-244 to render animation
                maze_num = filename.split(".")[0]
                maze_num = maze_num[len(maze_num)-1]
                title = "Maze " + str(maze_num) + " Solved With Greedy"
                fig, ax = render(states[0], title)

                def animate(i):
                    ax.clear()
                    ax.pcolormesh(states[i])
                    plt.xticks([]); plt.yticks([])
                    plt.title(title)

                # The animation has to be assigned to a variable to work
                animation = FuncAnimation(fig, animate, frames=len(states), interval=100, repeat=False)
                plt.show()

                path.reverse() # We reverse since we're backtracking
                print("[Greedy] The maze has been solved with these " + str(len(path)) + " steps: " + str(path) + "\n")
                print("[Greedy] The number of explored nodes is " + str(len(visited)) + ".\n")
                return path

            for action in ["U", "D", "L", "R"]:
                next_state = current_state.copy()
                curr_pos = next_state.index("2") # We're finding the current position of the start node (agent)

                if action == "U" and (min <= curr_pos - maze_width <= max) and next_state[curr_pos - maze_width] != '1': 
                    next_state[curr_pos] = '0'; next_state[curr_pos - maze_width] = '2'
                elif action == "D" and (min <= curr_pos + maze_width <= max) and next_state[curr_pos + maze_width] != '1': 
                    next_state[curr_pos] = '0'; next_state[curr_pos + maze_width] = '2'
                elif action == "L" and (min <= curr_pos - 1 <= max) and next_state[curr_pos - 1] != '1':
                    next_state[curr_pos] = '0'; next_state[curr_pos - 1] = '2'
                elif action == "R" and (min <= curr_pos + 1 <= max) and next_state[curr_pos + 1] != '1':
                    next_state[curr_pos] = '0'; next_state[curr_pos + 1] = '2'
                
                starter_coords = find_coordinates(next_state, maze_width, "2")
                next_state = "".join(s for s in next_state) # We convert the 1D array to a string
                if next_state not in visited:
                    visited.add(next_state) # We add the string form of the new state to the set

                    next_state = [s for s in next_state]
                    # We create our child node - Node(parent, action, state, depth, cost)
                    h = abs(starter_coords[0] - goal_coords[0]) + abs(starter_coords[1] - goal_coords[1])
                    # heap_priority_queue will be sorted by it's f(n), which is h(n)
                    heapq.heappush(heap_priority_queue, Node(current_node, action, next_state, current_node.depth + 1, h))

    print("The maze could not be solved!")
    return None
#------------------------------------- A-Star Implementation -------------------------------------

'''
In the TXT files, please note the following:
    2 means the agent
    3 means goal node
'''

def AStar_Maze_Solver(maze, filename): # Input is a 2D array with floats created with create_data(...)
    maze_width = len(maze[0])
    flattened = [str(int(c)) for r in maze for c in r] # 2D to 1D array

    starter_coords = find_coordinates(flattened, maze_width, "2")
    goal_coords = find_coordinates(flattened, maze_width, "3")
    g=0; h = abs(starter_coords[0] - goal_coords[0]) + abs(starter_coords[1] - goal_coords[1])

    '''
    Heuristic Used: f(n) = g(n) + h(n)
    g(n) = The distance (depth level) of the starter node to current node. (g)
    h(n) = The Manhattan distance of the current node to goal node (h) 
    '''

    starter_node = Node(None, None, flattened, g, g+h) # f(n) = g(n) + h(n) is our cost here
    heap_priority_queue = [starter_node]
    heapq.heapify(heap_priority_queue)
    
    starter_node = "".join(flattened)
    maze_area = len(starter_node)
    visited = {starter_node}
    min = 0; max = len(starter_node) - 1
    while heap_priority_queue:
        queue_size = len(heap_priority_queue)
        for _ in range(queue_size):
            current_node = heapq.heappop(heap_priority_queue)
            current_state = current_node.state

            if '3' not in current_state:
                path = []
                states = []
                while current_node.parent != None: # We're backtracking to compute the path
                    path.append(current_node.action)
                    
                    current_state = []
                    a = 0; b = maze_width
                    while b < maze_area + maze_width:
                        current_state.append([float(current_node.state[i]) for i in range(a,b)])
                        a += maze_width; b += maze_width

                    current_state.reverse()
                    states.append(current_state)
                    current_node = current_node.parent
                
                initial_maze = maze.copy(); initial_maze.reverse()
                states.append(initial_maze)
                states.reverse()

                prev = []
                for s in states:
                    if prev:
                        for x,y in prev:
                            s[x][y] = 3.0
                    prev.append(find_coordinates(s, maze_width, 2.0))
                
                # Uncomment Lines 234-244 to render animation
                maze_num = filename.split(".")[0]
                maze_num = maze_num[len(maze_num)-1]
                title = "Maze " + str(maze_num) + " Solved With A-Star"
                fig, ax = render(states[0], title)

                def animate(i):
                    ax.clear()
                    ax.pcolormesh(states[i])
                    plt.xticks([]); plt.yticks([])
                    plt.title(title)

                # The animation has to be assigned to a variable to work
                animation = FuncAnimation(fig, animate, frames=len(states), interval=100, repeat=False)
                plt.show()

                path.reverse() # We reverse since we're backtracking
                print("[A-Star] The maze has been solved with these " + str(len(path)) + " steps: " + str(path) + "\n")
                print("[A-Star] The number of explored nodes is " + str(len(visited)) + ".\n")
                return path

            for action in ["U", "D", "L", "R"]:
                next_state = current_state.copy()
                curr_pos = next_state.index("2") # We're finding the current position of the start node (agent)

                if action == "U" and (min <= curr_pos - maze_width <= max) and next_state[curr_pos - maze_width] != '1': 
                    next_state[curr_pos] = '0'; next_state[curr_pos - maze_width] = '2'
                elif action == "D" and (min <= curr_pos + maze_width <= max) and next_state[curr_pos + maze_width] != '1': 
                    next_state[curr_pos] = '0'; next_state[curr_pos + maze_width] = '2'
                elif action == "L" and (min <= curr_pos - 1 <= max) and next_state[curr_pos - 1] != '1':
                    next_state[curr_pos] = '0'; next_state[curr_pos - 1] = '2'
                elif action == "R" and (min <= curr_pos + 1 <= max) and next_state[curr_pos + 1] != '1':
                    next_state[curr_pos] = '0'; next_state[curr_pos + 1] = '2'
                
                starter_coords = find_coordinates(next_state, maze_width, "2")
                next_state = "".join(s for s in next_state) # We convert the 1D array to a string
                if next_state not in visited:
                    visited.add(next_state) # We add the string form of the new state to the set

                    next_state = [s for s in next_state]
                    # We create our child node - Node(parent, action, state, depth, cost)
                    g = current_node.depth + 1
                    h = abs(starter_coords[0] - goal_coords[0]) + abs(starter_coords[1] - goal_coords[1])
                    # heap_priority_queue will be sorted by it's f(n), which is g(n) + h(n)
                    heapq.heappush(heap_priority_queue, Node(current_node, action, next_state, g, g+h))

    print("The maze could not be solved!")
    return None