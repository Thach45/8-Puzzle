from flask import render_template
import time
from .andor_search_controller import (
    get_valid_moves, move, are_states_equal, is_goal, 
    state_to_tuple, manhattan_distance
)
from .no_observation_controller import (
    get_valid_actions_for_belief, apply_action_to_belief
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
            next_belief, _ = apply_action_to_belief(current_belief, action)
            
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