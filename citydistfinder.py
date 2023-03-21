import tkinter as tk
from tkinter import ttk
import math
from collections import defaultdict
came_from = defaultdict(list)

'''
SHORT NAMES OF CITY:
VA: Vancouver
NV: North Vancouver
WB: West Vancouver
B: Burnaby
R: Richmond
S: Surrey
NWM: New Westminster
D: Delta
LG: Langley
A: Abbotsford
L: Chilliwack
H: Hope
M: Mission
'''

# define the graph with the cost value
graph = {
    'VA': {'NV': 12, 'WB': 10, 'B': 8},
    'NV': {'VA': 12, 'WB': 5},
    'WB': {'VA': 10, 'NV': 5, 'B': 7, 'R': 6},
    'B': {'VA': 8, 'WB': 7, 'R': 5, 'S': 10},
    'R': {'WB': 6, 'B': 5, 'S': 8, 'NWM': 10},
    'S': {'B': 10, 'R': 8, 'NWM': 6, 'LG': 14, 'D': 12},
    'NWM': {'R': 10, 'S': 6, 'LG': 8, 'D': 8},
    'LG': {'S': 14, 'NWM': 8, 'A': 18},
    'D': {'S': 12, 'NWM': 8, 'A': 15, 'L': 20},
    'A': {'LG': 18, 'D': 15, 'L': 5},
    'L': {'A': 5, 'D': 20, 'H': 18},
    'H': {'L': 18}
}

# define the heuristic function
heuristic = {
    'VA': 40,
    'NV': 32,
    'WB': 30,
    'B': 28,
    'R': 20,
    'S': 15,
    'NWM': 12,
    'LG': 10,
    'D': 8,
    'A': 5,
    'L': 3,
    'H': 0
}

#dijkstra algorithm
def dijkstra(start, end):
    open_set = {start}
    closed_set = set()
    g_scores = {node: math.inf for node in graph}
    g_scores[start] = 0

    while open_set:
        current = min(open_set, key=lambda node: g_scores[node])
        if current == end:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return list(reversed(path))
        open_set.remove(current)
        closed_set.add(current)

        for neighbor, distance in graph[current].items():
            if neighbor in closed_set:
                continue
            tentative_g_score = g_scores[current] + distance
            if tentative_g_score < g_scores[neighbor]:
                came_from[neighbor] = current
                g_scores[neighbor] = tentative_g_score
                if neighbor not in open_set:
                    open_set.add(neighbor)

    return None

#grassfire algorithm
def grassfire(start, end):
    frontier = [start]
    closed_set = set()
    distance = {node: math.inf for node in graph}
    distance[start] = 0

    while frontier:
        current = frontier.pop(0)
        if current == end:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return list(reversed(path))
        closed_set.add(current)

        for neighbor in graph[current]:
            if neighbor in closed_set:
                continue
            if distance[current] + graph[current][neighbor] < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = distance[current] + graph[current][neighbor]
                if neighbor not in frontier:
                    frontier.append(neighbor)

    return None

# A* algorithm
def PathFinder(start, end, algorithm):
    open_set = {start}
    closed_set = set()
    g_scores = {node: math.inf for node in graph}
    g_scores[start] = 0
    f_scores = {node: math.inf for node in graph}
    f_scores[start] = heuristic[start]

    while open_set:
        current = min(open_set, key=lambda node: f_scores[node])
        if current == end:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return list(reversed(path))
        open_set.remove(current)
        closed_set.add(current)

        for neighbor, distance in graph[current].items():
            if neighbor in closed_set:
                continue
            tentative_g_score = g_scores[current] + distance
            if tentative_g_score < g_scores[neighbor]:
                came_from[neighbor] = current
                g_scores[neighbor] = tentative_g_score
                f_scores[neighbor] = g_scores[neighbor] + heuristic[neighbor]
                if neighbor not in open_set:
                    open_set.add(neighbor)

    return None

# create the window
window = tk.Tk()
window.title("Input Form")
window.geometry("300x300")

# create the label and input field for the first input
label_1 = ttk.Label(window, text="Starting City")
label_1.pack(pady=5)
input_1 = ttk.Entry(window)
input_1.pack(pady=5)

# create the label and input field for the second input
label_2 = ttk.Label(window, text="Goal City")
label_2.pack(pady=5)
input_2 = ttk.Entry(window)
input_2.pack(pady=5)

# create the radio button
algorithm_var = tk.StringVar(value="A*")
radio_button = ttk.Radiobutton(window, text="A*", variable=algorithm_var, value="A*")
radio_button.pack(pady=5)
radio_button = ttk.Radiobutton(window, text="Grassfire", variable=algorithm_var, value="Grassfire")
radio_button.pack(pady=5)
radio_button = ttk.Radiobutton(window, text="Dijkstra's", variable=algorithm_var, value="Dijkstra's")
radio_button.pack(pady=5)

# create the button to submit the form
def submit_form():
    start_city = input_1.get()
    end_city = input_2.get()
    algorithm = algorithm_var.get()
    
    if algorithm=="A*":
        path = PathFinder(start_city, end_city, algorithm)
    elif algorithm=="Grassfire":
        path =  grassfire(start_city,end_city)
    elif algorithm=="Dijkstra's":
        path = dijkstra(start_city,end_city)
        
        
    if path:
        result = " -> ".join(path)
    else:
        result = "No path found"
    result_label.config(text=result)
    

submit_button = ttk.Button(window, text="Submit", command=submit_form)
submit_button.pack(pady=10)

result_label = tk.Label(window, text="Result: ")
result_label.pack()
# run the window
window.mainloop()

