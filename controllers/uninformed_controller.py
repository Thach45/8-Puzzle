from flask import render_template, jsonify
from models.model import Model
from collections import deque
import heapq
import time

def home_controller():
    model = Model()
    data = model.get_data()
    return render_template('home.html', data=data)

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
    # Handle both list and tuple representations
    if isinstance(state[0], tuple):
        # Convert to list of lists for modification
        new_state = [list(row) for row in state]
    else:
        # Create a deep copy if it's already a list
        new_state = [row[:] for row in state]
    
    i, j = blank_pos
    di, dj = move
    new_i, new_j = i + di, j + dj
    new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
    
    # Return in the same format as input (list or tuple)
    if isinstance(state[0], tuple):
        return tuple(tuple(row) for row in new_state)
    return new_state

def state_to_string(state):
    """Convert a state to a string for visited set."""
    return ''.join(str(num) for row in state for num in row)

def bfs_controller():
    # Initial and goal states
    initial_state = [[2, 8, 3],
                    [1, 6, 4],
                    [7, 0, 5]]
    
    goal_state = [[1, 2, 3],
                  [8, 0, 4], 
                  [7, 6, 5]]
    
    start_time = time.time()
    result = bfs_search(initial_state, goal_state)
    end_time = time.time()
    
    execution_time = round(end_time - start_time, 4)
    
    if result is None:
        return jsonify({
            'status': 'error',
            'message': 'No solution found'
        })
    
    path, nodes_explored = result
    
    # Convert nested lists to strings for JSON serialization
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
    print(data)
    return render_template('bfs.html', data=data)

def bfs_search(initial_state, goal_state, max_iterations=100000):
    """
    Breadth-First Search implementation for the 8-puzzle problem.
    
    Args:
        initial_state: The starting state of the puzzle
        goal_state: The target state to reach
        max_iterations: Maximum number of nodes to explore
        
    Returns:
        (path, nodes_explored) if solution found, None otherwise
    """
    if initial_state == goal_state:
        return [initial_state], 1
    
    # Convert states to tuples for hashability
    initial_tuple = tuple(tuple(row) for row in initial_state)
    goal_tuple = tuple(tuple(row) for row in goal_state)
    
    queue = deque([(initial_tuple, [initial_tuple])])
    visited = {initial_tuple}
    nodes_explored = 0
    
    while queue and nodes_explored < max_iterations:
        current_state, path = queue.popleft()
        nodes_explored += 1
        
        blank_i, blank_j = get_blank_position(current_state)
        possible_moves = get_possible_moves(blank_i, blank_j)
        
        for move in possible_moves:
            new_state = get_new_state(current_state, move, (blank_i, blank_j))
            
            if new_state not in visited:
                if new_state == goal_tuple:
                    # Convert tuples back to lists for the final path
                    return [list(map(list, state)) for state in path + [new_state]], nodes_explored
                
                visited.add(new_state)
                queue.append((new_state, path + [new_state]))
    
    return None

def dfs_controller():
    # Initial and goal states
    initial_state = [[2, 8, 3],
                    [1, 6, 4],
                    [7, 0, 5]]
    
    goal_state = [[1, 2, 3],
                  [8, 0, 4], 
                  [7, 6, 5]]
    
    start_time = time.time()
    result = dfs_search(initial_state, goal_state)
    end_time = time.time()
    
    execution_time = round(end_time - start_time, 4)
    
    if result is None:
        return jsonify({
            'status': 'error',
            'message': 'No solution found'
        })
    
    path, nodes_explored = result
    
    # Convert nested lists to strings for JSON serialization
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
    print(data)
    return render_template('dfs.html', data=data)

def dfs_search(initial_state, goal_state, max_depth=30, max_iterations=100000):
    """
    Depth-First Search implementation with depth limit for the 8-puzzle problem.
    
    Args:
        initial_state: The starting state of the puzzle
        goal_state: The target state to reach
        max_depth: Maximum depth to search
        max_iterations: Maximum number of nodes to explore
        
    Returns:
        (path, nodes_explored) if solution found, None otherwise
    """
    # Convert states to tuples for hashability
    initial_tuple = tuple(tuple(row) for row in initial_state)
    goal_tuple = tuple(tuple(row) for row in goal_state)
    
    stack = [(initial_tuple, [initial_tuple], 0)]  # (state, path, depth)
    visited = {initial_tuple}
    nodes_explored = 0
    
    while stack and nodes_explored < max_iterations:
        current_state, path, depth = stack.pop()
        nodes_explored += 1
        
        if current_state == goal_tuple:
            # Convert tuples back to lists for the final path
            return [list(map(list, state)) for state in path], nodes_explored
        
        if depth < max_depth:  # Limit search depth to prevent exponential explosion
            blank_i, blank_j = get_blank_position(current_state)
            possible_moves = get_possible_moves(blank_i, blank_j)
            
            # Explore moves in reverse to maintain expected DFS order
            for move in reversed(possible_moves):
                new_state = get_new_state(current_state, move, (blank_i, blank_j))
                
                if new_state not in visited:
                    visited.add(new_state)
                    stack.append((new_state, path + [new_state], depth + 1))
    
    return None

def ucs_controller():
    # Initial and goal states
    initial_state = [[2, 8, 3],
                    [1, 6, 4],
                    [7, 0, 5]]
    
    goal_state = [[1, 2, 3],
                  [8, 0, 4], 
                  [7, 6, 5]]
    
    start_time = time.time()
    result = ucs_search(initial_state, goal_state)
    end_time = time.time()
    
    execution_time = round(end_time - start_time, 4)
    
    if result is None:
        return jsonify({
            'status': 'error',
            'message': 'No solution found'
        })
    
    path, nodes_explored = result
    
    # Convert nested lists to strings for JSON serialization
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
    print(data)
    return render_template('ucs.html', data=data)

def ucs_search(initial_state, goal_state, max_iterations=100000):
    """
    Uniform Cost Search implementation for the 8-puzzle problem using heapq.
    
    Args:
        initial_state: The starting state of the puzzle
        goal_state: The target state to reach
        max_iterations: Maximum number of nodes to explore
        
    Returns:
        (path, nodes_explored) if solution found, None otherwise
    """
    # Convert states to tuples for hashability
    initial_tuple = tuple(tuple(row) for row in initial_state)
    goal_tuple = tuple(tuple(row) for row in goal_state)
    
    # Priority queue with (cost, counter, state, path)
    # Counter is used to break ties when costs are equal
    counter = 0
    queue = [(0, counter, initial_tuple, [initial_tuple])]
    visited = {initial_tuple}
    nodes_explored = 0
    
    while queue and nodes_explored < max_iterations:
        cost, _, current_state, path = heapq.heappop(queue)
        nodes_explored += 1
        
        if current_state == goal_tuple:
            # Convert tuples back to lists for the final path
            return [list(map(list, state)) for state in path], nodes_explored
        
        blank_i, blank_j = get_blank_position(current_state)
        possible_moves = get_possible_moves(blank_i, blank_j)
        
        for move in possible_moves:
            new_state = get_new_state(current_state, move, (blank_i, blank_j))
            
            if new_state not in visited:
                visited.add(new_state)
                new_cost = cost + 1  # Assuming each move has a cost of 1
                counter += 1
                heapq.heappush(queue, (new_cost, counter, new_state, path + [new_state]))
    
    return None

def iddfs_controller():
    # Initial and goal states
    initial_state = [ [1, 2, 3],
                        [0, 4, 6],
                        [7, 5, 8]]
    
    goal_state = [[1, 2, 3],
                  [4, 5, 6], 
                  [7, 8, 0]]
    
    start_time = time.time()
    result = id_dfs_search(initial_state, goal_state)
    end_time = time.time()
    
    execution_time = round(end_time - start_time, 4)
    
    if result is None:
        return jsonify({
            'status': 'error',
            'message': 'No solution found'
        })
    
    path, nodes_explored = result
    
    # Convert nested lists to strings for JSON serialization
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
    print(data)
    return render_template('iddfs.html', data=data)

def id_dfs_search(initial_state, goal_state, max_depth=130):
    """
    Iterative Deepening Depth-First Search implementation for the 8-puzzle problem.
    
    Args:
        initial_state: The starting state of the puzzle
        goal_state: The target state to reach
        max_depth: Maximum depth to search
        
    Returns:
        (path, nodes_explored) if solution found, None otherwise
    """
    # Convert states to tuples for hashability
    initial_tuple = tuple(tuple(row) for row in initial_state)
    goal_tuple = tuple(tuple(row) for row in goal_state)
    
    total_nodes_explored = 0
    
    for depth in range(max_depth):
        visited = set()  # Reset visited set for each depth iteration
        result, nodes = depth_limited_search(initial_tuple, goal_tuple, depth, visited)
        total_nodes_explored += nodes
        
        if result is not None:
            # Convert tuples back to lists for the final path
            return [list(map(list, state)) for state in result], total_nodes_explored
    
    return None

def depth_limited_search(initial_state, goal_state, depth_limit, visited):
    """
    Depth-Limited Search helper function for IDDFS.
    
    Args:
        initial_state: The starting state of the puzzle
        goal_state: The target state to reach
        depth_limit: Maximum depth to search
        visited: Set of visited states
        
    Returns:
        (path, nodes_explored) if solution found, (None, nodes_explored) otherwise
    """
    stack = [(initial_state, [initial_state], 0)]  # (state, path, depth)
    visited.add(initial_state)
    nodes_explored = 0
    
    while stack:
        current_state, path, depth = stack.pop()
        nodes_explored += 1
        
        if current_state == goal_state:
            return path, nodes_explored
        
        if depth < depth_limit:
            blank_i, blank_j = get_blank_position(current_state)
            possible_moves = get_possible_moves(blank_i, blank_j)
            
            # Explore moves in reverse to maintain expected DFS order
            for move in reversed(possible_moves):
                new_state = get_new_state(current_state, move, (blank_i, blank_j))
                
                if new_state not in visited:
                    visited.add(new_state)
                    stack.append((new_state, path + [new_state], depth + 1))
    
    return None, nodes_explored

# Optional: Add A* search algorithm
def astar_controller():
    # Initial and goal states
    initial_state = [[2, 8, 3],
                    [1, 6, 4],
                    [7, 0, 5]]
    
    goal_state = [[1, 2, 3],
                  [8, 0, 4], 
                  [7, 6, 5]]
    
    start_time = time.time()
    result = astar_search(initial_state, goal_state)
    end_time = time.time()
    
    execution_time = round(end_time - start_time, 4)
    
    if result is None:
        return jsonify({
            'status': 'error',
            'message': 'No solution found'
        })
    
    path, nodes_explored = result
    
    # Convert nested lists to strings for JSON serialization
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
    print(data)
    return render_template('astar.html', data=data)

def manhattan_distance(state, goal_state):
    """
    Calculate the Manhattan distance heuristic between the current state and the goal state.
    """
    distance = 0
    goal_positions = {}
    
    # Find positions of each tile in the goal state
    for i in range(3):
        for j in range(3):
            if goal_state[i][j] != 0:  # Skip the blank tile
                goal_positions[goal_state[i][j]] = (i, j)
    
    # Calculate Manhattan distance for each tile
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:  # Skip the blank tile
                goal_i, goal_j = goal_positions[state[i][j]]
                distance += abs(i - goal_i) + abs(j - goal_j)
    
    return distance

def astar_search(initial_state, goal_state, max_iterations=100000):
    """
    A* Search implementation for the 8-puzzle problem.
    
    Args:
        initial_state: The starting state of the puzzle
        goal_state: The target state to reach
        max_iterations: Maximum number of nodes to explore
        
    Returns:
        (path, nodes_explored) if solution found, None otherwise
    """
    # Convert states to tuples for hashability
    initial_tuple = tuple(tuple(row) for row in initial_state)
    goal_tuple = tuple(tuple(row) for row in goal_state)
    
    # Convert goal state to list format for Manhattan distance calculation
    goal_list = [list(row) for row in goal_tuple]
    
    # Priority queue with (f_score, counter, g_score, state, path)
    # f_score = g_score + h_score, where g_score is the cost so far and h_score is the heuristic
    counter = 0
    h_score = manhattan_distance([list(row) for row in initial_tuple], goal_list)
    queue = [(h_score, counter, 0, initial_tuple, [initial_tuple])]
    visited = {initial_tuple: 0}  # State -> g_score
    nodes_explored = 0
    
    while queue and nodes_explored < max_iterations:
        _, _, g_score, current_state, path = heapq.heappop(queue)
        nodes_explored += 1
        
        if current_state == goal_tuple:
            # Convert tuples back to lists for the final path
            return [list(map(list, state)) for state in path], nodes_explored
        
        # Skip if we've found a better path to this state
        if current_state in visited and visited[current_state] < g_score:
            continue
        
        blank_i, blank_j = get_blank_position(current_state)
        possible_moves = get_possible_moves(blank_i, blank_j)
        
        for move in possible_moves:
            new_state = get_new_state(current_state, move, (blank_i, blank_j))
            new_g_score = g_score + 1  # Cost of one step
            
            # Skip if we've found a better path to this state
            if new_state in visited and visited[new_state] <= new_g_score:
                continue
                
            visited[new_state] = new_g_score
            h_score = manhattan_distance([list(row) for row in new_state], goal_list)
            f_score = new_g_score + h_score
            counter += 1
            heapq.heappush(queue, (f_score, counter, new_g_score, new_state, path + [new_state]))
    
    return None