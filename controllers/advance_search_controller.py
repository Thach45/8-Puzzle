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
    # Khi thực hiện một hành động, có thể trượt sang một hướng khác
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

    # Nếu không có trạng thái nào thay đổi, trả về trạng thái hiện tại
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

def and_or_search(initial_state, goal_state, max_depth=50):
    nodes_explored = 0
    memo = {}  # Để ghi nhớ các trạng thái đã thăm
    
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

    def or_search(state, depth):
        nonlocal nodes_explored
        nodes_explored += 1
        
        # Kiểm tra nếu đạt đến trạng thái đích
        if is_goal(state, goal_state):
            return True, {}
            
        # Kiểm tra giới hạn độ sâu
        if depth >= max_depth:
            return False, {}
            
        # Chuyển state thành tuple để sử dụng làm key
        state_tuple = state_to_tuple(state)
        
        # Nếu đã có kết quả cho trạng thái này, trả về kết quả đó
        if state_tuple in memo:
            return memo[state_tuple]
        
        # Sắp xếp các hành động theo khoảng cách Manhattan đến mục tiêu
        valid_moves = get_valid_moves(state)
        moves_with_distance = []
        for action in valid_moves:
            next_states = simulate_nondeterministic(state, action)
            min_distance = min(manhattan_distance(s, goal_state) for s in next_states)
            moves_with_distance.append((action, min_distance))
        
        # Sắp xếp theo khoảng cách tăng dần
        moves_with_distance.sort(key=lambda x: x[1])
        
        # Thử các hành động theo thứ tự ưu tiên
        for action, _ in moves_with_distance:
            next_states = simulate_nondeterministic(state, action)
            solved, subplan = and_search(next_states, depth + 1)
            
            if solved:
                plan = {state_tuple: (action, subplan)}
                memo[state_tuple] = (True, plan)
                return True, plan
        
        memo[state_tuple] = (False, {})
        return False, {}

    def and_search(states, depth):
        if not states:
            return True, {}
            
        # Kết hợp kết quả của tất cả các trạng thái
        combined_plan = {}
        for state in states:
            solved, plan = or_search(state, depth)
            if not solved:
                return False, {}
            combined_plan.update(plan)
        
        return True, combined_plan

    # Bắt đầu tìm kiếm từ trạng thái ban đầu
    start_time = time.time()
    solved, solution_graph = or_search(initial_state, 0)
    end_time = time.time()
    
    # Nếu tìm thấy lời giải, xây dựng đường đi
    solution_path = []
    if solved:
        current_state = initial_state
        current_tuple = state_to_tuple(current_state)
        solution_path.append(current_state)
        
        # Giới hạn số bước để tránh lặp vô hạn
        step_limit = 200  # Tăng giới hạn số bước
        step_count = 0
        visited = set()
        
        while current_tuple in solution_graph and step_count < step_limit:
            if current_tuple in visited:
                break
            visited.add(current_tuple)
            
            action, subgraph = solution_graph[current_tuple]
            next_states = simulate_nondeterministic(current_state, action)
            
            # Chọn trạng thái tiếp theo có trong subgraph hoặc gần với mục tiêu nhất
            next_state = None
            min_distance = float('inf')
            
            # Ưu tiên các trạng thái có trong subgraph
            for state in next_states:
                state_tuple = state_to_tuple(state)
                if state_tuple in subgraph:
                    next_state = state
                    break
            
            # Nếu không có trạng thái nào trong subgraph, chọn trạng thái gần mục tiêu nhất
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
    
    return solution_path, nodes_explored, len(solution_path) - 1, end_time - start_time

def andor_controller():
    # Sử dụng trạng thái đơn giản hơn - nhưng vẫn đủ thách thức
    initial_state = [[1, 2, 3],
                     [4, 0, 6],
                     [7, 5, 8]]

    goal_state = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 0, 8]]

    # Sử dụng max_depth cao hơn cho môi trường bất định
    solution, nodes, steps, exec_time = and_or_search(initial_state, goal_state, max_depth=30)

    if not solution or len(solution) <= 1 or not are_states_equal(solution[-1], goal_state):
        return jsonify({
            'status': 'error',
            'message': 'No solution found',
            'details': f'Explored {nodes} nodes, solution length: {len(solution)}'
        })

    return render_template('andor.html',
                           solution=solution,
                           nodes=nodes,
                           steps=steps,
                           time=round(exec_time, 3),
                           initial_state=initial_state)

def get_all_possible_outcomes(state, action):
    """
    Lấy tất cả các trạng thái có thể sau khi thực hiện một hành động
    Trong môi trường không quan sát:
    1. Hành động thành công (thực hiện đúng hành động)
    2. Hành động thất bại (giữ nguyên trạng thái)
    """
    outcomes = set()
    
    # 1. Thực hiện hành động
    intended_outcome = move(state, action)
    if not are_states_equal(intended_outcome, state):  # Chỉ thêm nếu thực sự thay đổi
        outcomes.add(state_to_tuple(intended_outcome))
    
    # 2. Giữ nguyên trạng thái (thất bại)
    outcomes.add(state_to_tuple(state))
    
    # Chuyển kết quả về dạng list of lists
    return [list(map(list, state)) for state in outcomes]

def is_action_applicable(belief_state, action):
    """Kiểm tra xem một hành động có thể áp dụng cho TẤT CẢ các trạng thái trong belief state không"""
    return all(action in get_valid_moves(state) for state in belief_state)

def get_valid_actions_for_belief(belief_state):
    """Lấy các hành động có thể áp dụng cho TẤT CẢ các trạng thái trong belief state"""
    if not belief_state:
        return []
    
    # Lấy tập hợp các hành động hợp lệ cho trạng thái đầu tiên
    valid_actions = set(get_valid_moves(belief_state[0]))
    
    # Lấy giao của tất cả các tập hợp hành động hợp lệ
    for state in belief_state[1:]:
        valid_actions &= set(get_valid_moves(state))
    
    return list(valid_actions)

def apply_action_to_belief(belief_state, action):
    """
    Áp dụng một hành động lên belief state và trả về belief state mới
    - Chỉ áp dụng hành động nếu nó khả thi cho TẤT CẢ các trạng thái
    - Với mỗi trạng thái, xem xét các kết quả có thể xảy ra
    - Loại bỏ các trạng thái trùng lặp
    """
    if not is_action_applicable(belief_state, action):
        return belief_state, []
    
    new_belief_states = set()
    transitions = []
    
    # Với mỗi trạng thái trong belief state hiện tại
    for state in belief_state:
        # Lấy tất cả các kết quả có thể
        possible_outcomes = get_all_possible_outcomes(state, action)
        
        # Thêm vào tập kết quả và ghi nhận chuyển đổi
        for outcome in possible_outcomes:
            new_belief_states.add(state_to_tuple(outcome))
            if not are_states_equal(state, outcome):  # Chỉ ghi nhận các chuyển đổi thực sự
                transitions.append((state, action, outcome))
    
    # Chuyển đổi kết quả về dạng list và sắp xếp để đảm bảo tính ổn định
    result = [list(map(list, state)) for state in new_belief_states]
    result.sort(key=lambda x: str(x))
    
    return result, transitions

def manhattan_distance(state1, state2):
    """Tính khoảng cách Manhattan giữa hai trạng thái"""
    distance = 0
    for i in range(3):
        for j in range(3):
            if state1[i][j] != 0:
                for x in range(3):
                    for y in range(3):
                        if state2[x][y] == state1[i][j]:
                            distance += abs(i - x) + abs(j - y)
                            break
    return distance

def is_belief_state_goal(belief_state, goal_state):
    """Kiểm tra xem TẤT CẢ các trạng thái trong belief state có phải là goal không"""
    return all(are_states_equal(state, goal_state) for state in belief_state)

def no_observation_search(initial_belief_state, goal_state, max_steps=50):
    """
    Thuật toán tìm kiếm không quan sát cho 8-puzzle
    - Chỉ chọn hành động khi nó áp dụng được cho TẤT CẢ các trạng thái trong belief state
    - Theo dõi tất cả các trạng thái có thể sau mỗi hành động
    - Dừng khi TẤT CẢ các trạng thái trong belief state là goal
    """
    queue = [(initial_belief_state, [])]  # (belief_state, actions)
    visited_beliefs = set()
    
    search_trace = [{
        'step': 0,
        'belief_state': initial_belief_state,
        'valid_actions': get_valid_actions_for_belief(initial_belief_state),
        'chosen_action': None,
        'transitions': [],
        'explanation': "Trạng thái niềm tin ban đầu"
    }]
    
    while queue and len(queue[0][1]) < max_steps:
        current_belief, actions = queue.pop(0)
        
        # Chuyển belief state thành dạng có thể hash
        belief_tuple = tuple(tuple(state_to_tuple(state)) for state in current_belief)
        if belief_tuple in visited_beliefs:
            continue
        visited_beliefs.add(belief_tuple)
        
        # Kiểm tra xem đã đạt goal chưa
        if is_belief_state_goal(current_belief, goal_state):
            search_trace.append({
                'step': len(actions),
                'belief_state': current_belief,
                'valid_actions': [],
                'chosen_action': None,
                'transitions': [],
                'explanation': "Đã đạt được trạng thái đích!"
            })
            return actions, search_trace
        
        # Lấy các hành động có thể áp dụng cho TẤT CẢ các trạng thái
        valid_actions = get_valid_actions_for_belief(current_belief)
        
        # Thử từng hành động
        for action in valid_actions:
            # Áp dụng hành động và lấy các kết quả có thể
            next_belief, transitions = apply_action_to_belief(current_belief, action)
            
            # Tính khoảng cách trung bình đến goal
            distances = [manhattan_distance(state, goal_state) for state in next_belief]
            avg_distance = sum(distances) / len(distances)
            
            # Nếu khoảng cách quá xa, bỏ qua
            if avg_distance > 20:
                continue
            
            # Thêm bước này vào trace
            search_trace.append({
                'step': len(actions) + 1,
                'belief_state': next_belief,
                'valid_actions': get_valid_actions_for_belief(next_belief),
                'chosen_action': action,
                'transitions': transitions,
                'explanation': f"Áp dụng hành động {action}. Số trạng thái có thể: {len(next_belief)}"
            })
            
            # Thêm vào queue để tiếp tục tìm kiếm
            next_belief_tuple = tuple(tuple(state_to_tuple(state)) for state in next_belief)
            if next_belief_tuple not in visited_beliefs:
                queue.append((next_belief, actions + [action]))
    
    return None, search_trace

# --- NO-OBSERVATION SEARCH: DETERMINISTIC BELIEF PROPAGATION ---
def get_all_possible_deterministic(state, action):
    """
    Chỉ xét hành động thành công (không có noise, không thất bại, không trượt).
    """
    return [move(state, action)]

def apply_action_to_belief_deterministic(belief_state, action):
    """
    Áp dụng một hành động lên belief state (deterministic):
    - Chỉ xét hành động thành công.
    - Loại bỏ trùng lặp.
    """
    if not is_action_applicable(belief_state, action):
        return belief_state, []
    new_belief = set()
    transitions = []
    for state in belief_state:
        next_state = move(state, action)
        new_belief.add(state_to_tuple(next_state))
        transitions.append((state, action, next_state))
    # Convert back to list of lists
    new_belief = [ [list(row) for row in state] for state in new_belief ]
    new_belief.sort(key=lambda x: str(x))
    return new_belief, transitions

def is_belief_state_goal(belief_state, goal_state):
    return all(are_states_equal(state, goal_state) for state in belief_state)

def no_observation_search_deterministic(initial_belief_state, goal_state, max_steps=50):
    """
    No-observation search: DFS/backtracking trên belief state.
    Ở mỗi bước, thử tất cả các action hợp lệ. Trả về trace của nhánh đầu tiên tìm được kết quả.
    Khi backtrack, thêm một bước trace với explanation rõ ràng.
    """
    from copy import deepcopy

    def belief_to_hashable(belief):
        return tuple(sorted(tuple(tuple(row) for row in state) for state in belief))

    def dfs(current_belief, actions, trace, step, visited_beliefs):
        if is_belief_state_goal(current_belief, goal_state):
            trace.append({
                'step': step,
                'belief_state_before': current_belief,
                'chosen_action': None,
                'belief_state_after': current_belief,
                'valid_actions': [],
                'transitions': [],
                'explanation': "Đã đạt trạng thái đích cho toàn bộ belief state!"
            })
            return actions, trace
        if step >= max_steps:
            trace.append({
                'step': step,
                'belief_state_before': current_belief,
                'chosen_action': None,
                'belief_state_after': current_belief,
                'valid_actions': [],
                'transitions': [],
                'explanation': "Vượt quá số bước tối đa."
            })
            return None, trace
        valid_actions = get_valid_actions_for_belief(current_belief)
        if not valid_actions:
            trace.append({
                'step': step,
                'belief_state_before': current_belief,
                'chosen_action': None,
                'belief_state_after': current_belief,
                'valid_actions': [],
                'transitions': [],
                'explanation': "Không còn hành động nào hợp lệ cho belief state hiện tại."
            })
            return None, trace
        visited_beliefs.add(belief_to_hashable(current_belief))
        found_solution = False
        for action in valid_actions:
            next_belief, transitions = apply_action_to_belief_deterministic(current_belief, action)
            next_hash = belief_to_hashable(next_belief)
            if next_hash in visited_beliefs:
                continue
            if set(tuple(map(tuple, s)) for s in next_belief) == set(tuple(map(tuple, s)) for s in current_belief):
                continue
            new_trace = deepcopy(trace)
            new_trace.append({
                'step': step,
                'belief_state_before': current_belief,
                'chosen_action': action,
                'belief_state_after': next_belief,
                'valid_actions': get_valid_actions_for_belief(next_belief),
                'transitions': transitions,
                'explanation': f"Áp dụng hành động {action}, belief state còn {len(next_belief)} trạng thái."
            })
            result = dfs(next_belief, actions + [action], new_trace, step + 1, visited_beliefs.copy())
            if result[0] is not None:
                return result
            # Nếu quay lui, thêm bước trace để thông báo
            new_trace.append({
                'step': step + 1,
                'belief_state_before': next_belief,
                'chosen_action': None,
                'belief_state_after': current_belief,
                'valid_actions': valid_actions,
                'transitions': [],
                'explanation': f"Backtracking: Quay lui từ belief state này về bước trước."
            })
        return None, trace

    actions, trace = dfs(initial_belief_state, [], [], 0, set())
    return actions, trace

def no_observation_controller():
    """Controller cho thuật toán tìm kiếm không quan sát với phiên bản deterministic"""
    # Chỉ sử dụng 2 trạng thái ban đầu gần nhau để tránh không gian tìm kiếm quá lớn
    initial_belief_state = [
        [[1, 2, 3],
         [4, 0, 6],
         [7, 5, 8]],
        [[1, 2, 3],
         [4, 5, 6],
         [7, 0, 8]]
    ]
    
    goal_state = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 0]]

    # Giới hạn số bước tìm kiếm để tránh treo
    max_steps = 20
    
    start_time = time.time()
    try:
        solution, search_trace = no_observation_search_deterministic(
            initial_belief_state, 
            goal_state,
            max_steps=max_steps
        )
        success = solution is not None
        message = "Tìm thấy lời giải!" if success else "Không tìm thấy lời giải trong giới hạn bước."
    except Exception as e:
        success = False
        message = f"Lỗi khi tìm kiếm: {str(e)}"
        search_trace = []
        solution = None
    finally:
        end_time = time.time()

    return render_template(
        'no_observation.html',
        search_trace=search_trace,
        solution=solution,
        time=round(end_time - start_time, 3),
        found_solution=success,
        message=message
    )

def get_observation(state, observable_positions):
    """
    Lấy quan sát từ trạng thái với các vị trí có thể quan sát được.
    observable_positions là list các tuple (row, col) có thể quan sát.
    Trả về một ma trận với các giá trị None ở vị trí không quan sát được.
    """
    observation = [[None for _ in range(3)] for _ in range(3)]
    for i, j in observable_positions:
        observation[i][j] = state[i][j]
    return observation

def is_observation_match(state, observation):
    """Kiểm tra xem một trạng thái có phù hợp với quan sát không"""
    for i in range(3):
        for j in range(3):
            if observation[i][j] is not None and observation[i][j] != state[i][j]:
                return False
    return True

def update_belief_with_observation(belief_state, observation):
    """Cập nhật belief state dựa trên quan sát mới"""
    new_belief = []
    for state in belief_state:
        if is_observation_match(state, observation):
            new_belief.append(state)
    return new_belief

def partial_observation_search(initial_belief_state, goal_state, observable_positions, max_steps=30):
    """
    Thuật toán tìm kiếm với quan sát một phần:
    - Tại mỗi bước:
        1. Quan sát các ô có thể thấy được
        2. Cập nhật belief state dựa trên quan sát
        3. Chọn hành động tốt nhất dựa trên belief state hiện tại
        4. Thực hiện hành động và cập nhật belief state
    - Dừng khi:
        1. Tất cả trạng thái trong belief state là goal, hoặc
        2. Không còn hành động hợp lệ, hoặc
        3. Belief state không thay đổi sau hành động
    """
    def belief_to_hashable(belief_state):
        """Chuyển belief state thành dạng tuple có thể hash"""
        return tuple(tuple(tuple(row) for row in state) for state in sorted(belief_state, key=str))

    def estimate_distance_to_goal(belief_state):
        """Ước tính khoảng cách đến goal dựa trên các ô đã biết"""
        total_distance = 0
        count = 0
        for state in belief_state:
            # Chỉ tính khoảng cách cho các ô quan sát được
            for i, j in observable_positions:
                if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                    # Tìm vị trí đích của số này trong goal
                    for x in range(3):
                        for y in range(3):
                            if goal_state[x][y] == state[i][j]:
                                total_distance += abs(i - x) + abs(j - y)
                                count += 1
                                break
        return total_distance / (count if count > 0 else 1)

    search_trace = [{
        'step': 0,
        'belief_state_before': initial_belief_state,
        'observation': get_observation(initial_belief_state[0], observable_positions),
        'chosen_action': None,
        'belief_state_after': initial_belief_state,
        'explanation': "Trạng thái niềm tin ban đầu"
    }]
    
    current_belief = initial_belief_state
    actions_taken = []
    visited_beliefs = {belief_to_hashable(initial_belief_state)}
    
    while len(actions_taken) < max_steps:
        # Lấy quan sát hiện tại
        current_observation = get_observation(current_belief[0], observable_positions)
        
        # Cập nhật belief state dựa trên quan sát
        current_belief = update_belief_with_observation(current_belief, current_observation)
        
        # Kiểm tra điều kiện dừng
        if all(is_goal(state, goal_state) for state in current_belief):
            search_trace.append({
                'step': len(actions_taken),
                'belief_state_before': current_belief,
                'observation': current_observation,
                'chosen_action': None,
                'belief_state_after': current_belief,
                'explanation': "Đã đạt được trạng thái đích!"
            })
            return actions_taken, search_trace
            
        # Lấy các hành động hợp lệ
        valid_actions = get_valid_actions_for_belief(current_belief)
        if not valid_actions:
            search_trace.append({
                'step': len(actions_taken),
                'belief_state_before': current_belief,
                'observation': current_observation,
                'chosen_action': None,
                'belief_state_after': current_belief,
                'explanation': "Không còn hành động hợp lệ!"
            })
            return None, search_trace
            
        # Chọn hành động tốt nhất
        best_action = None
        min_distance = float('inf')
        best_next_belief = None
        
        for action in valid_actions:
            # Thử hành động
            next_belief, _ = apply_action_to_belief_deterministic(current_belief, action)
            
            # Lấy quan sát mới
            next_observation = get_observation(next_belief[0], observable_positions)
            updated_belief = update_belief_with_observation(next_belief, next_observation)
            
            if not updated_belief:
                continue
                
            # Đánh giá hành động dựa trên các ô quan sát được
            distance = estimate_distance_to_goal(updated_belief)
            
            if distance < min_distance:
                min_distance = distance
                best_action = action
                best_next_belief = updated_belief
        
        if best_action is None:
            search_trace.append({
                'step': len(actions_taken),
                'belief_state_before': current_belief,
                'observation': current_observation,
                'chosen_action': None,
                'belief_state_after': current_belief,
                'explanation': "Không tìm thấy hành động tốt!"
            })
            return None, search_trace
            
        # Kiểm tra belief state mới
        next_belief_hash = belief_to_hashable(best_next_belief)
        if next_belief_hash in visited_beliefs:
            search_trace.append({
                'step': len(actions_taken),
                'belief_state_before': current_belief,
                'observation': current_observation,
                'chosen_action': None,
                'belief_state_after': current_belief,
                'explanation': "Đã thăm belief state này trước đó!"
            })
            return None, search_trace
            
        # Cập nhật trạng thái
        current_belief = best_next_belief
        actions_taken.append(best_action)
        visited_beliefs.add(next_belief_hash)
        
        # Ghi nhận bước thực hiện
        search_trace.append({
            'step': len(actions_taken),
            'belief_state_before': current_belief,
            'observation': current_observation,
            'chosen_action': best_action,
            'belief_state_after': best_next_belief,
            'explanation': (f"Thực hiện {best_action}. Quan sát thấy {len(observable_positions)} ô. "
                          f"Belief state còn {len(best_next_belief)} trạng thái khả thi.")
        })
    
    search_trace.append({
        'step': len(actions_taken),
        'belief_state_before': current_belief,
        'observation': get_observation(current_belief[0], observable_positions),
        'chosen_action': None,
        'belief_state_after': current_belief,
        'explanation': "Đã đạt đến giới hạn số bước!"
    })
    return None, search_trace

def partial_observation_controller():
    """Controller cho thuật toán tìm kiếm với quan sát một phần"""
    # Trạng thái ban đầu và đích
    initial_belief_state = [
        [[1, 2, 3],
         [4, 0, 6],
         [7, 5, 8]],
        [[1, 2, 3],
         [4, 5, 6],
         [7, 0, 8]]
    ]
    
    goal_state = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 0]]
    
    # Chỉ có thể quan sát được một số ô
    # Ví dụ: có thể thấy các góc và ô giữa
    observable_positions = [
        (0, 0), (0, 2),  # Góc trên
        (1, 1),          # Ô giữa
        (2, 0), (2, 2)   # Góc dưới
    ]
    
    max_steps = 20  # Giới hạn số bước để tránh treo
    
    start_time = time.time()
    try:
        solution, search_trace = partial_observation_search(
            initial_belief_state,
            goal_state,
            observable_positions,
            max_steps=max_steps
        )
        success = solution is not None
        message = "Tìm thấy lời giải!" if success else "Không tìm thấy lời giải trong giới hạn bước."
    except Exception as e:
        success = False
        message = f"Lỗi khi tìm kiếm: {str(e)}"
        search_trace = []
        solution = None
    finally:
        end_time = time.time()
    
    return render_template(
        'partial_observation.html',
        search_trace=search_trace,
        solution=solution,
        time=round(end_time - start_time, 3),
        found_solution=success,
        message=message,
        observable_positions=observable_positions
    )

