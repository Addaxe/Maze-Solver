import matplotlib.pyplot as plt

def graph(title, xlabel, ylabel, ydata1, ydata2, ydata3, ydata4, label1, label2, label3, label4):
    x = [1,2,3,4]

    plt.plot(x, ydata1, marker = 'o', label = label1)
    plt.plot(x, ydata2, marker = 'o', label = label2)
    plt.plot(x, ydata3, marker = 'o', label = label3)
    plt.plot(x, ydata4, marker = 'o', label = label4)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.xticks(x, ["Maze 1","Maze 2", "Maze 3", "Maze 4"])
    plt.legend()
    plt.grid()
    plt.show()

#------------------------------------- Number of Steps Per Maze For Every Search-------------------------------------

BFS_ydata = [118, 78, 124, 188]
DFS_ydata = [118, 78, 124, 596]
Greedy_ydata = [118, 78, 124, 228]
AStar_ydata = [118, 78, 124, 188]

graph("Number of Steps Per Maze For Every Search ", "Maze Number", "Number of Steps", BFS_ydata, DFS_ydata, Greedy_ydata, AStar_ydata, "BFS", "DFS", "Greedy", "A Star")

#------------------------------------- Number of Nodes Explored Per Maze For Every Search -------------------------------------

BFS_ydata = [201, 183, 239, 1673]
DFS_ydata = [141, 94, 174, 806]
Greedy_ydata = [197, 123, 175, 316]
AStar_ydata = [201, 147, 185, 1641]

graph("Number of Nodes Explored Per Maze For Every Search ", "Maze Number", "Number of Nodes Explored", BFS_ydata, DFS_ydata, Greedy_ydata, AStar_ydata, "BFS", "DFS", "Greedy", "A Star")

#------------------------------------- Execution Time Per Maze For Every Search -------------------------------------

BFS_ydata = [12.713142156600952, 8.558846950531006, 13.216531038284302, 22.410685300827026]
DFS_ydata = [12.818583011627197, 8.377255916595459, 13.066412687301636, 66.282949924469]
Greedy_ydata = [12.662762880325317, 8.295349836349487, 13.199717998504639, 25.530656099319458]
AStar_ydata = [12.516599893569946, 8.45918583869934, 13.399671077728271, 26.728153944015503]

graph("Execution Time Per Maze For Every Search ", "Maze Number", "Execution Time", BFS_ydata, DFS_ydata, Greedy_ydata, AStar_ydata, "BFS", "DFS", "Greedy", "A Star")