# importing required libraries
import random
import numpy as np
import tkinter as tk

def grassfire(grid, start_point, goal):
    # Get the number of rows and columns in the grid
    rows, cols = np.shape(grid)
    
    # Initialize an array "distances" with infinity values except for the starting point
    distances = np.full((rows, cols), np.inf)
    distances[start_point[0], start_point[1]] = 0
    
    # Create a queue with the starting point
    queue = [start_point]
    
    while queue:
        # Pop the first item from the queue as the current point
        curr = queue.pop(0)
        row, col = curr[0], curr[1]
        
        # If the current point is equal to the goal, break the loop
        if curr == goal:
            break
        
        # Calculate the neighboring cells of the current point
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        
        # For each neighbor, check if it's not an obstacle and its distance is not set yet
        for neighbor in neighbors:
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] != 1:
                if distances[neighbor[0], neighbor[1]] == np.inf:
                    # Update the distance to the neighbor and add it to the queue
                    distances[neighbor[0], neighbor[1]] = distances[row, col] + 1
                    queue.append(neighbor)
                    
    return distances


def generate_search_map(rows, cols, obs_percent):
    # create a 2D grid with zeros of size rows x cols
    grid = np.zeros((rows, cols))
    
    # calculate the number of obstacles based on the percentage of obstacles 
    # specified by the user, rounded down to the nearest integer
    obs_num = int(rows * cols * obs_percent / 100)

    # randomly select obs_num number of cells to be obstacles
    for i in range(obs_num):
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        grid[row][col] = 1

    # get the start and goal points from the user inputs
    start_point = (int(start_row_entry.get()), int(start_col_entry.get()))
    goal = (int(goal_row_entry.get()), int(goal_col_entry.get()))

    return grid, start_point, goal


def calculate_path():
    rows = int(row_entry.get())
    cols = int(col_entry.get())
    obs_percent = int(obs_entry.get())
    
    # Generate the search map, including the grid, start point, and goal point
    grid, start_point, goal = generate_search_map(rows, cols, obs_percent)
    
    # Get the distances from the start point to each cell using the Grassfire algorithm
    distances = grassfire(grid, start_point, goal)
    
    # Calculate the shortest path from the goal to the start point
    path = []
    row, col = goal
    path = [(row, col)]
    while (row, col) != start_point:
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        min_distance = np.inf
        for neighbor in neighbors:
            # Check if the neighbor is within the grid boundary
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                # Choose the neighbor with the minimum distance
                if distances[neighbor[0], neighbor[1]] < min_distance:
                    min_distance = distances[neighbor[0], neighbor[1]]
                    row, col = neighbor
        path.append((row, col))
                    
    path.reverse()
    
    # Display the result and draw the path on the GUI
    result_label.config(text=f"Shortest path = {path}")
    draw_path(path, grid, start_point, goal)


def draw_path(path, grid, start_point, goal):
    # Draws the grid, start and goal points and path using a Tkinter canvas.
    canvas.delete("all") # Clears previous drawings in the canvas
    
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            # Check if cell is an obstacle, start point or goal point
            if grid[row][col] == 1:
                color = "black"
            elif (row, col) == start_point:
                color = "green"
            elif (row, col) == goal:
                color = "red"
            else:
                color = "white"
                
            # Draws the cell in the canvas with specified color
            canvas.create_rectangle(col * cell_size, row * cell_size,(col + 1) * cell_size, (row + 1) * cell_size, fill=color)
            
    root.mainloop()

# Create a Tkinter GUI window    
root = tk.Tk()
root.title("Grassfire Search")
cell_size = 20

# Create a Tkinter frame to display results
result_frame = tk.Frame(root)
result_frame.grid(row=0, column=0, sticky="nsew")

result_label = tk.Label(result_frame, text="Your Answer Is :", font=("Helvetica", 16), wraplength=220,foreground=
                        'red')
result_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
result_frame.grid_rowconfigure(0, weight=1)
result_frame.grid_columnconfigure(0, weight=1)

# Create a canvas to draw graph
canvas = tk.Canvas(root, height=180, width=180, bg="white")
canvas.grid(row=1, column=0)

input_frame = tk.Frame(root)
input_frame.grid(row=2, column=0, sticky="nsew")

row_label = tk.Label(input_frame, text="Rows:", font=("Helvetica", 12))
row_label.grid(row=0, column=0, pady=10)
row_entry = tk.Entry(input_frame, font=("Helvetica", 12))
row_entry.grid(row=0, column=1, pady=10)

col_label = tk.Label(input_frame, text="Columns:", font=("Helvetica", 12))
col_label.grid(row=1, column=0, pady=10)
col_entry = tk.Entry(input_frame, font=("Helvetica", 12))
col_entry.grid(row=1, column=1, pady=10)

obs_label = tk.Label(input_frame, text="Obstacle Percentage:", font=("Helvetica", 12))
obs_label.grid(row=2, column=0, pady=10)
obs_entry = tk.Entry(input_frame, font=("Helvetica", 12))
obs_entry.grid(row=2, column=1, pady=10)

start_row_label = tk.Label(input_frame, text="Start Point Row:", font=("Helvetica", 12))
start_row_label.grid(row=3, column=0, pady=10)
start_row_entry = tk.Entry(input_frame, font=("Helvetica", 12))
start_row_entry.grid(row=3, column=1, pady=10)

start_col_label = tk.Label(input_frame, text="Start Point Column:", font=("Helvetica", 12))
start_col_label.grid(row=4, column=0, pady=10)
start_col_entry = tk.Entry(input_frame, font=("Helvetica", 12))
start_col_entry.grid(row=4, column=1, pady=10)

goal_row_label = tk.Label(input_frame, text="Goal Row:", font=("Helvetica", 12))
goal_row_label.grid(row=5, column=0, pady=10)
goal_row_entry = tk.Entry(input_frame, font=("Helvetica", 12))
goal_row_entry.grid(row=5, column=1, pady=10)

goal_col_label = tk.Label(input_frame, text="Goal Column:", font=("Helvetica", 12))
goal_col_label.grid(row=6, column=0, pady=10)
goal_col_entry = tk.Entry(input_frame, font=("Helvetica", 12))
goal_col_entry.grid(row=6, column=1, pady=10)

calculate_button = tk.Button(root, text="Calculate Path", command=calculate_path, bg="black", fg="white", font=("Helvetica", 12))
calculate_button.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()