import numpy as np
import matplotlib.pyplot as plt

def manhattan_distance(state, goal):
    distance = 0
    for i in range(1, 9):  
        xi, yi = np.where(state == i)
        xg, yg = np.where(goal == i)
        distance += abs(xi[0] - xg[0]) + abs(yi[0] - yg[0]) 
    return int(distance)

def get_neighbors(state):
    neighbors = []
    x, y = np.where(state == 0)
    x, y = x[0], y[0]
    moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for nx, ny in moves:
        if 0 <= nx < 3 and 0 <= ny < 3:  # Ensure valid move
            new_state = state.copy()
            new_state[x, y], new_state[nx, ny] = new_state[nx, ny], new_state[x, y]
            neighbors.append(new_state)
    return neighbors

def hill_climbing_with_full_values(initial, goal, heuristic):
    current_state = initial
    current_cost = heuristic(current_state, goal)
    steps = [(current_state, current_cost)]
    all_heuristic_values = []  # To track all possible heuristic values
    
    while True:
        neighbors = get_neighbors(current_state)
        neighbors_with_costs = [(neighbor, heuristic(neighbor, goal)) for neighbor in neighbors]
        all_heuristic_values.extend([cost for _, cost in neighbors_with_costs]) 
        neighbors_with_costs = sorted(neighbors_with_costs, key=lambda x: x[1])  
        if not neighbors_with_costs or neighbors_with_costs[0][1] >= current_cost:  
            break
        
        current_state, current_cost = neighbors_with_costs[0]
        steps.append((current_state, current_cost))
        
        # Check if goal state is reached
        if current_cost == 0:
            break
    
    return steps, all_heuristic_values

def plot_full_objective_vs_state_space(all_heuristic_values):
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(all_heuristic_values)), all_heuristic_values, marker='o', linestyle='-', color='blue', label='Heuristic Values')
    plt.title("Objective Function vs State Space")
    plt.xlabel("State Space (Indexed by Visit Order)")
    plt.ylabel("Objective Function (Heuristic Value)")
    plt.legend()
    plt.grid()
    plt.show()

def get_user_input():
    print("Enter the initial configuration row by row, separated by spaces.")
    print("Use 0 to represent the blank tile.")
    initial = []
    for i in range(3):
        row = input(f"Row {i + 1}: ").strip().split()
        initial.append([int(x) for x in row])
    return np.array(initial)

if __name__ == "__main__":
    initial = get_user_input()
    goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    steps, all_heuristic_values = hill_climbing_with_full_values(initial, goal, heuristic=manhattan_distance)
    
    for idx, (state, cost) in enumerate(steps):
        print(f"Step {idx} - Cost: {cost}\n{state}\n")
    
    if steps[-1][1] == 0:
        print("Goal state reached!\n")
        print(steps[-1][0])
    
    plot_full_objective_vs_state_space(all_heuristic_values)