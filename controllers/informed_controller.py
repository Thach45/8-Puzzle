from flask import render_template, jsonify
from models.model import Model
from collections import deque
import heapq
import time

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

def greedy_controller():
    """Controller for Greedy Best-First Search."""
    initial_state = [[2, 8, 3],
                    [1, 6, 4],
                    [7, 0, 5]]
    
    goal_state = [[1, 2, 3],
                  [8, 0, 4],
                  [7, 6, 5]]
    
    start_time = time.time()
    result = greedy_search(initial_state, goal_state)
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
    return render_template('greedy.html', data=data)

def greedy_search(initial_state, goal_state, max_iterations=100000):
    """Greedy Best-First Search implementation."""
    initial_tuple = tuple(tuple(row) for row in initial_state)
    goal_tuple = tuple(tuple(row) for row in goal_state)
    goal_list = [list(row) for row in goal_tuple]
    
    counter = 0
    h_score = manhattan_distance([list(row) for row in initial_tuple], goal_list)
    queue = [(h_score, counter, initial_tuple, [initial_tuple])]
    visited = {initial_tuple}
    nodes_explored = 0
    
    while queue and nodes_explored < max_iterations:
        _, _, current_state, path = heapq.heappop(queue)
        nodes_explored += 1
        
        if current_state == goal_tuple:
            return [list(map(list, state)) for state in path], nodes_explored
        
        blank_i, blank_j = get_blank_position(current_state)
        possible_moves = get_possible_moves(blank_i, blank_j)
        
        for move in possible_moves:
            new_state = get_new_state(current_state, move, (blank_i, blank_j))
            
            if new_state not in visited:
                visited.add(new_state)
                h_score = manhattan_distance([list(row) for row in new_state], goal_list)
                counter += 1
                heapq.heappush(queue, (h_score, counter, new_state, path + [new_state]))
    
    return None

def a_star_controller():
    """Controller for A* Search."""
    initial_state = [[2, 8, 3],
                    [1, 6, 4],
                    [7, 0, 5]]
    
    goal_state = [[1, 2, 3],
                  [8, 0, 4],
                  [7, 6, 5]]
    
    start_time = time.time()
    result = a_star_search(initial_state, goal_state)
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
    return render_template('astar.html', data=data)

def a_star_search(initial_state, goal_state, max_iterations=100000):
    """A* Search implementation."""
    initial_tuple = tuple(tuple(row) for row in initial_state)
    goal_tuple = tuple(tuple(row) for row in goal_state)
    goal_list = [list(row) for row in goal_tuple]
    
    counter = 0
    h_score = manhattan_distance([list(row) for row in initial_tuple], goal_list)
    queue = [(h_score, counter, 0, initial_tuple, [initial_tuple])]  # f_score, counter, g_score, state, path
    visited = {initial_tuple: 0}  # State -> g_score
    nodes_explored = 0
    
    while queue and nodes_explored < max_iterations:
        _, _, g_score, current_state, path = heapq.heappop(queue)
        nodes_explored += 1
        
        if current_state == goal_tuple:
            return [list(map(list, state)) for state in path], nodes_explored
        
        blank_i, blank_j = get_blank_position(current_state)
        possible_moves = get_possible_moves(blank_i, blank_j)
        
        for move in possible_moves:
            new_state = get_new_state(current_state, move, (blank_i, blank_j))
            new_g_score = g_score + 1
            
            if new_state not in visited or new_g_score < visited[new_state]:
                visited[new_state] = new_g_score
                h_score = manhattan_distance([list(row) for row in new_state], goal_list)
                f_score = new_g_score + h_score
                counter += 1
                heapq.heappush(queue, (f_score, counter, new_g_score, new_state, path + [new_state]))
    
    return None

def ida_star_controller():
    """Controller for IDA* Search."""
    initial_state = [[2, 8, 3],
                    [1, 6, 4],
                    [7, 0, 5]]
    
    goal_state = [[1, 2, 3],
                  [8, 0, 4],
                  [7, 6, 5]]
    
    start_time = time.time()
    result = ida_star_search(initial_state, goal_state)
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
    return render_template('idastar.html', data=data)

def ida_star_search(initial_state, goal_state, max_iterations=100000):
    """IDA* Search implementation."""
    initial_tuple = tuple(tuple(row) for row in initial_state)
    goal_tuple = tuple(tuple(row) for row in goal_state)
    goal_list = [list(row) for row in goal_tuple]
    
    def search(path, g_score, bound, nodes):
        current = path[-1]
        f_score = g_score + manhattan_distance([list(row) for row in current], goal_list)
        
        if f_score > bound:
            return f_score, None, nodes
        
        if current == goal_tuple:
            return True, path, nodes
        
        min_cost = float('inf')
        nodes += 1
        
        if nodes >= max_iterations:
            return None, None, nodes
        
        blank_i, blank_j = get_blank_position(current)
        possible_moves = get_possible_moves(blank_i, blank_j)
        
        for move in possible_moves:
            new_state = get_new_state(current, move, (blank_i, blank_j))
            if new_state not in path:
                path.append(new_state)
                result, new_path, new_nodes = search(path, g_score + 1, bound, nodes)
                nodes = new_nodes
                
                if result is True:
                    return True, new_path, nodes
                if result is not None:
                    min_cost = min(min_cost, result)
                    
                path.pop()
        
        return min_cost, None, nodes
    
    h_score = manhattan_distance([list(row) for row in initial_tuple], goal_list)
    bound = h_score
    nodes_explored = 0
    
    while True:
        path = [initial_tuple]
        result, solution_path, nodes = search(path, 0, bound, nodes_explored)
        nodes_explored = nodes
        
        if result is True:
            return [list(map(list, state)) for state in solution_path], nodes_explored
        if result is None or result == float('inf'):
            return None
        
        bound = result

def beam_search_controller():
    """Controller for Beam Search."""
    initial_state = [[2, 8, 3],
                    [1, 6, 4],
                    [7, 0, 5]]
    
    goal_state = [[1, 2, 3],
                  [8, 0, 4],
                  [7, 6, 5]]
    
    start_time = time.time()
    result = beam_search(initial_state, goal_state)
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
    return render_template('beam.html', data=data)

def beam_search(initial_state, goal_state, beam_width=3, max_iterations=100000):
    """Beam Search implementation."""
    initial_tuple = tuple(tuple(row) for row in initial_state)
    goal_tuple = tuple(tuple(row) for row in goal_state)
    goal_list = [list(row) for row in goal_tuple]
    
    current_beam = [(manhattan_distance([list(row) for row in initial_tuple], goal_list), 
                    initial_tuple, [initial_tuple])]
    visited = {initial_tuple}
    nodes_explored = 0
    
    while current_beam and nodes_explored < max_iterations:
        next_beam = []
        
        for _, current_state, path in current_beam:
            nodes_explored += 1
            
            if current_state == goal_tuple:
                return [list(map(list, state)) for state in path], nodes_explored
            
            blank_i, blank_j = get_blank_position(current_state)
            possible_moves = get_possible_moves(blank_i, blank_j)
            
            for move in possible_moves:
                new_state = get_new_state(current_state, move, (blank_i, blank_j))
                
                if new_state not in visited:
                    visited.add(new_state)
                    h_score = manhattan_distance([list(row) for row in new_state], goal_list)
                    next_beam.append((h_score, new_state, path + [new_state]))
        
        if not next_beam:
            break
            
        # Keep only the best beam_width states
        next_beam.sort()  # Sort by h_score
        current_beam = next_beam[:beam_width]
    
    return None