from flask import render_template, jsonify
import time

def get_valid_moves(state):
    """Get all valid moves for current state"""
    valid_moves = []
    blank_pos = None

    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                blank_pos = (i, j)
                break
        if blank_pos:
            break

    i, j = blank_pos
    if i > 0: valid_moves.append('up')
    if i < 2: valid_moves.append('down')
    if j > 0: valid_moves.append('left')
    if j < 2: valid_moves.append('right')

    return valid_moves

def move(state, action):
    """Execute a move on the given state"""
    new_state = [row[:] for row in state]
    
    blank_pos = None
    for i in range(3):
        for j in range(3):
            if new_state[i][j] == 0:
                blank_pos = (i, j)
                break
        if blank_pos is not None:
            break

    if blank_pos is None:
        raise ValueError("Không tìm thấy ô trống trong trạng thái")

    i, j = blank_pos

    if action == 'up' and i > 0:
        new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]
    elif action == 'down' and i < 2:
        new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
    elif action == 'left' and j > 0:
        new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
    elif action == 'right' and j < 2:
        new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]

    return new_state

def simulate_nondeterministic(state, action):
    """Mô phỏng môi trường bất định"""
    possible_states = []

    # Hành động chính xác (95% xác suất)
    main_state = move(state, action)
    if not are_states_equal(main_state, state):
        possible_states.append(main_state)

    # Chỉ xét một hành động không mong muốn (5% xác suất)
    slide_actions = {
        'up': ['left'],
        'down': ['right'],
        'left': ['up'],
        'right': ['down']
    }

    # Thêm trạng thái có thể xảy ra khi trượt
    for slide_action in slide_actions.get(action, []):
        slide_state = move(state, slide_action)
        if not are_states_equal(slide_state, state) and not any(are_states_equal(slide_state, s) for s in possible_states):
            possible_states.append(slide_state)

    return possible_states if possible_states else [state]

def are_states_equal(state1, state2):
    """Kiểm tra hai trạng thái có bằng nhau không"""
    return all(state1[i][j] == state2[i][j] for i in range(3) for j in range(3))

def is_goal(state, goal_state):
    """Kiểm tra có phải là trạng thái đích không"""
    return are_states_equal(state, goal_state)

def state_to_tuple(state):
    """Chuyển state thành tuple để có thể sử dụng làm key"""
    return tuple(tuple(row) for row in state)

def manhattan_distance(state1, state2):
    """Tính khoảng cách Manhattan giữa hai trạng thái"""
    distance = 0
    for i in range(3):
        for j in range(3):
            if state1[i][j] != 0:  # Bỏ qua ô trống
                # Tìm vị trí của số trong state2
                for x in range(3):
                    for y in range(3):
                        if state2[x][y] == state1[i][j]:
                            distance += abs(i - x) + abs(j - y)
                            break
    return distance

def and_or_search(initial_state, goal_state, max_depth=50):
    nodes_explored = 0
    memo = {}  # Để ghi nhớ các trạng thái đã thăm
    search_steps = []  # Lưu trữ các bước tìm kiếm
    
    def add_search_step(step_type, state, valid_actions=None, chosen_action=None, 
                       next_states=None, success=None, explanation=None):
        """Thêm một bước tìm kiếm vào danh sách các bước"""
        # Đảm bảo state là list nếu là single state
        if isinstance(state, list) and not isinstance(state[0], list):
            state = [state]
            
        step = {
            'type': step_type,
            'state': state[0] if isinstance(state, list) and len(state) > 0 else state,  # Lấy state đầu tiên nếu là list states
            'valid_actions': valid_actions if valid_actions is not None else [],
            'chosen_action': chosen_action,
            'next_states': next_states if next_states is not None else [],
            'success': success if success is not None else False,
            'explanation': explanation if explanation is not None else ""
        }
        search_steps.append(step)
    
    def or_search(state, depth):
        nonlocal nodes_explored
        nodes_explored += 1
        
        # Kiểm tra trạng thái đích
        if is_goal(state, goal_state):
            add_search_step('or', state, success=True,
                          explanation="Đạt được trạng thái đích!")
            return True, {}
        
        # Kiểm tra giới hạn độ sâu
        if depth >= max_depth:
            add_search_step('or', state, success=False,
                          explanation=f"Đạt đến giới hạn độ sâu {max_depth}")
            return False, {}
        
        state_tuple = state_to_tuple(state)
        if state_tuple in memo:
            result, plan = memo[state_tuple]
            add_search_step('or', state, success=result,
                          explanation="Trạng thái này đã được thăm trước đó")
            return result, plan
        
        # Lấy và sắp xếp các hành động theo khoảng cách Manhattan
        valid_moves = get_valid_moves(state)
        moves_with_distance = []
        for action in valid_moves:
            next_states = simulate_nondeterministic(state, action)
            min_distance = min(manhattan_distance(s, goal_state) for s in next_states)
            moves_with_distance.append((action, min_distance))
        
        moves_with_distance.sort(key=lambda x: x[1])
        valid_actions = [action for action, _ in moves_with_distance]
        
        add_search_step('or', state, valid_actions=valid_actions,
                       explanation="Đang xem xét các hành động khả thi")
        
        # Thử các hành động theo thứ tự ưu tiên
        for action, _ in moves_with_distance:
            next_states = simulate_nondeterministic(state, action)
            
            add_search_step('and', state, chosen_action=action, next_states=next_states,
                          explanation=f"Thử hành động {action}")
            
            solved, subplan = and_search(next_states, depth + 1)
            
            if solved:
                add_search_step('or', state, chosen_action=action, success=True,
                              explanation=f"Hành động {action} dẫn đến thành công")
                plan = {state_tuple: (action, subplan)}
                memo[state_tuple] = (True, plan)
                return True, plan
            
            add_search_step('or', state, chosen_action=action, success=False,
                          explanation=f"Hành động {action} không thành công")
        
        memo[state_tuple] = (False, {})
        return False, {}
    
    def and_search(states, depth):
        if not states:
            return True, {}
        
        # Kết hợp kết quả của tất cả các trạng thái
        combined_plan = {}
        all_solved = True
        
        for state in states:
            add_search_step('and', state,
                          explanation="Xử lý trạng thái trong AND node")
            
            solved, plan = or_search(state, depth)
            if not solved:
                all_solved = False
                add_search_step('and', state, success=False,
                              explanation="Một trạng thái trong AND node thất bại")
                break
            
            combined_plan.update(plan)
        
        if all_solved:
            add_search_step('and', states[0], success=True,
                          explanation="Tất cả trạng thái trong AND node thành công")
        
        return all_solved, combined_plan
    
    # Bắt đầu tìm kiếm
    start_time = time.time()
    solved, solution_graph = or_search(initial_state, 0)
    end_time = time.time()
    
    # Xây dựng đường đi nếu tìm thấy lời giải
    solution_path = []
    if solved:
        current_state = initial_state
        current_tuple = state_to_tuple(current_state)
        solution_path.append(current_state)
        
        step_limit = 200
        step_count = 0
        visited = set()
        
        while current_tuple in solution_graph and step_count < step_limit:
            if current_tuple in visited:
                break
            visited.add(current_tuple)
            
            action, subgraph = solution_graph[current_tuple]
            next_states = simulate_nondeterministic(current_state, action)
            
            next_state = None
            min_distance = float('inf')
            
            for state in next_states:
                state_tuple = state_to_tuple(state)
                if state_tuple in subgraph:
                    next_state = state
                    break
            
            if next_state is None:
                for state in next_states:
                    if is_goal(state, goal_state):
                        next_state = state
                        break
                    distance = manhattan_distance(state, goal_state)
                    if distance < min_distance:
                        min_distance = distance
                        next_state = state
            
            if next_state is None:
                break
            
            current_state = next_state
            current_tuple = state_to_tuple(current_state)
            solution_path.append(current_state)
            step_count += 1
            
            if is_goal(current_state, goal_state):
                break
    
    # Đảm bảo solution_path không rỗng
    if not solution_path:
        solution_path = [initial_state]
    
    tree_data = {
        'steps': search_steps,
        'nodesExplored': nodes_explored,
        'searchDepth': max_depth,
        'execTime': round(end_time - start_time, 3),
        'success': solved
    }
    
    return solution_path, nodes_explored, len(solution_path) - 1, end_time - start_time, tree_data

def andor_controller():
    initial_state = [[1, 2, 3],
                     [4, 0, 6],
                     [7, 5, 8]]

    goal_state = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 0, 8]]

    solution, nodes, steps, exec_time, tree_data = and_or_search(initial_state, goal_state, max_depth=30)
    found = solution and len(solution) > 1 and are_states_equal(solution[-1], goal_state)

    # Đảm bảo tất cả các giá trị được khởi tạo
    if not tree_data.get('steps'):
        tree_data['steps'] = []
    
    return render_template('andor_tree.html',
                         tree_data=tree_data,
                         solution=solution if solution else [initial_state],
                         nodes=nodes if nodes is not None else 0,
                         steps=steps if steps is not None else 0,
                         time=round(exec_time, 3) if exec_time is not None else 0,
                         initial_state=initial_state,
                         found=found) 