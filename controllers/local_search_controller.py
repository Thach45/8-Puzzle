from flask import render_template, jsonify
import random
import math
import time
import copy

def get_blank_position(state):
    """Find the position of the blank (0) in the puzzle state."""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_possible_moves(i, j):
    """Get all possible moves from the current blank position."""
    moves = []
    if i > 0: moves.append((-1, 0))  # up
    if i < 2: moves.append((1, 0))   # down
    if j > 0: moves.append((0, -1))  # left
    if j < 2: moves.append((0, 1))   # right
    return moves

def get_new_state(state, move, blank_pos):
    """Create a new state by moving the blank tile."""
    if isinstance(state[0], tuple):
        new_state = [list(row) for row in state]
    else:
        new_state = [row[:] for row in state]
    
    i, j = blank_pos
    di, dj = move
    new_i, new_j = i + di, j + dj
    new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
    
    if isinstance(state[0], tuple):
        return tuple(tuple(row) for row in new_state)
    return new_state

def manhattan_distance(state, goal_state):
    """Calculate Manhattan distance heuristic."""
    distance = 0
    goal_positions = {}
    
    for i in range(3):
        for j in range(3):
            if goal_state[i][j] != 0:
                goal_positions[goal_state[i][j]] = (i, j)
    
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                goal_i, goal_j = goal_positions[state[i][j]]
                distance += abs(i - goal_i) + abs(j - goal_j)
    
    return distance

def simple_hill_climbing_controller():
    """Controller for Simple Hill Climbing Search."""
    initial_state = [[2, 8, 3],
                    [1, 6, 4],
                    [7, 0, 5]]
    
    goal_state = [[1, 2, 3],
                  [8, 0, 4],
                  [7, 6, 5]]
    
    start_time = time.time()
    result = simple_hill_climbing_search(initial_state, goal_state)
    end_time = time.time()
    
    execution_time = round(end_time - start_time, 4)
    
    if result is None:
        return jsonify({
            'status': 'error',
            'message': 'No solution found'
        })
    
    path, nodes_explored = result
    path = [[[str(cell) for cell in row] for row in state] for state in path]
    
    data = {
        'status': 'success',
        'path': path,
        'path_length': len(path),
        'nodes_explored': nodes_explored,
        'execution_time': execution_time,
        'initial_state': initial_state,
        'goal_state': goal_state
    }
    return render_template('hill_climbing.html', data=data)

def simple_hill_climbing_search(initial_state, goal_state, max_iterations=100):
    """Simple Hill Climbing Search implementation - takes first improvement."""
    current_state = [row[:] for row in initial_state]
    path = [current_state]
    nodes_explored = 0
    
    while nodes_explored < max_iterations:
        current_score = manhattan_distance(current_state, goal_state)
        
        if current_score == 0:  # Goal state reached
            return path, nodes_explored
        
        blank_i, blank_j = get_blank_position(current_state)
        possible_moves = get_possible_moves(blank_i, blank_j)
        found_better = False
        
        for move in possible_moves:
            nodes_explored += 1
            neighbor = get_new_state(current_state, move, (blank_i, blank_j))
            neighbor_score = manhattan_distance(neighbor, goal_state)
            
            if neighbor_score < current_score:  # Take first improvement
                current_state = [row[:] for row in neighbor]
                path.append(current_state)
                found_better = True
                break
        
        if not found_better:  # Local maximum reached
            return path, nodes_explored
    
    return None

def steepest_hill_climbing_controller():
    """Controller for Steepest-Ascent Hill Climbing Search."""
    initial_state = [[2, 8, 3],
                    [1, 6, 4],
                    [7, 0, 5]]
    
    goal_state = [[1, 2, 3],
                  [8, 0, 4],
                  [7, 6, 5]]
    
    start_time = time.time()
    result = steepest_hill_climbing_search(initial_state, goal_state)
    end_time = time.time()
    
    execution_time = round(end_time - start_time, 4)
    
    if result is None:
        return jsonify({
            'status': 'error',
            'message': 'No solution found'
        })
    
    path, nodes_explored = result
    path = [[[str(cell) for cell in row] for row in state] for state in path]
    
    data = {
        'status': 'success',
        'path': path,
        'path_length': len(path),
        'nodes_explored': nodes_explored,
        'execution_time': execution_time,
        'initial_state': initial_state,
        'goal_state': goal_state
    }
    return render_template('steepest_hill_climbing.html', data=data)

def steepest_hill_climbing_search(initial_state, goal_state, max_iterations=100):
    """Steepest-Ascent Hill Climbing Search implementation - chooses best improvement."""
    current_state = [row[:] for row in initial_state]
    path = [current_state]
    nodes_explored = 0
    
    while nodes_explored < max_iterations:
        current_score = manhattan_distance(current_state, goal_state)
        
        if current_score == 0:  # Goal state reached
            return path, nodes_explored
            
        blank_i, blank_j = get_blank_position(current_state)
        possible_moves = get_possible_moves(blank_i, blank_j)
        best_neighbor = None
        best_score = current_score
        
        for move in possible_moves:
            nodes_explored += 1
            neighbor = get_new_state(current_state, move, (blank_i, blank_j))
            neighbor_score = manhattan_distance(neighbor, goal_state)
            
            if neighbor_score < best_score:
                best_neighbor = neighbor
                best_score = neighbor_score
        
        if best_neighbor is None:  # Local maximum reached
            return path, nodes_explored
            
        current_state = [row[:] for row in best_neighbor]
        path.append(current_state)
    
    return None

def stochastic_hill_climbing_controller():
    """Controller for Stochastic Hill Climbing Search."""
    initial_state = [[2, 8, 3],
                    [1, 6, 4],
                    [7, 0, 5]]
    
    goal_state = [[1, 2, 3],
                  [8, 0, 4],
                  [7, 6, 5]]
    
    start_time = time.time()
    result = stochastic_hill_climbing_search(initial_state, goal_state)
    end_time = time.time()
    
    execution_time = round(end_time - start_time, 4)
    
    if result is None:
        return jsonify({
            'status': 'error',
            'message': 'No solution found'
        })
    
    path, nodes_explored = result
    path = [[[str(cell) for cell in row] for row in state] for state in path]
    
    data = {
        'status': 'success',
        'path': path,
        'path_length': len(path),
        'nodes_explored': nodes_explored,
        'execution_time': execution_time,
        'initial_state': initial_state,
        'goal_state': goal_state
    }
    return render_template('stochastic_hill_climbing.html', data=data)

def stochastic_hill_climbing_search(initial_state, goal_state, max_iterations=100):
    """Stochastic Hill Climbing Search implementation - randomly selects among better neighbors."""
    current_state = [row[:] for row in initial_state]
    path = [current_state]
    nodes_explored = 0
    
    while nodes_explored < max_iterations:
        current_score = manhattan_distance(current_state, goal_state)
        
        if current_score == 0:  # Goal state reached
            return path, nodes_explored
            
        blank_i, blank_j = get_blank_position(current_state)
        possible_moves = get_possible_moves(blank_i, blank_j)
        better_neighbors = []
        
        for move in possible_moves:
            nodes_explored += 1
            neighbor = get_new_state(current_state, move, (blank_i, blank_j))
            neighbor_score = manhattan_distance(neighbor, goal_state)
            
            if neighbor_score < current_score:
                better_neighbors.append(neighbor)
        
        if not better_neighbors:  # Local maximum reached
            return path, nodes_explored
            
        # Randomly select one of the better neighbors
        current_state = [row[:] for row in random.choice(better_neighbors)]
        path.append(current_state)
    
    return None

def simulated_annealing_controller():
    """Controller for Simulated Annealing Search."""
    initial_state = [[2, 8, 3],
                    [1, 6, 4],
                    [7, 0, 5]]
    
    goal_state = [[1, 2, 3],
                  [8, 0, 4],
                  [7, 6, 5]]
    
    start_time = time.time()
    result = simulated_annealing_search(initial_state, goal_state)
    end_time = time.time()
    
    execution_time = round(end_time - start_time, 4)
    
    if result is None:
        return jsonify({
            'status': 'error',
            'message': 'No solution found'
        })
    
    path, nodes_explored = result
    path = [[[str(cell) for cell in row] for row in state] for state in path]
    
    data = {
        'status': 'success',
        'path': path,
        'path_length': len(path),
        'nodes_explored': nodes_explored,
        'execution_time': execution_time,
        'initial_state': initial_state,
        'goal_state': goal_state
    }
    return render_template('simulated_annealing.html', data=data)

def simulated_annealing_search(initial_state, goal_state, max_iterations=1000, initial_temp=1.0, cooling_rate=0.995):
    """Simulated Annealing Search implementation."""
    current_state = [row[:] for row in initial_state]
    path = [current_state]
    nodes_explored = 0
    temperature = initial_temp
    
    while nodes_explored < max_iterations and temperature > 0.01:
        current_score = manhattan_distance(current_state, goal_state)
        
        if current_score == 0:  # Goal state reached
            return path, nodes_explored
        
        blank_i, blank_j = get_blank_position(current_state)
        possible_moves = get_possible_moves(blank_i, blank_j)
        
        # Select random move
        move = random.choice(possible_moves)
        nodes_explored += 1
        
        new_state = get_new_state(current_state, move, (blank_i, blank_j))
        new_score = manhattan_distance(new_state, goal_state)
        
        # Calculate acceptance probability
        delta_e = new_score - current_score
        if delta_e < 0 or random.random() < math.exp(-delta_e / temperature):
            current_state = [row[:] for row in new_state]
            path.append(current_state)
        
        temperature *= cooling_rate
    
    return None