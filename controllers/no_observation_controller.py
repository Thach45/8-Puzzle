from flask import render_template, jsonify
import time
from .andor_search_controller import (
    get_valid_moves, move, are_states_equal, is_goal
)

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
    """
    new_belief_state = []
    transitions = []
    
    # Thực hiện action trên từng state
    for state in belief_state:
        if action in get_valid_moves(state):
            new_state = move(state, action)
            new_belief_state.append(new_state)
            if not are_states_equal(state, new_state):
                transitions.append((state, action, new_state))
            
    return new_belief_state, transitions

def get_filtered_belief_state(belief_state, action):
    """
    Lọc và trả về belief state mới chỉ gồm các states có thể thực hiện được action.
    Đồng thời trả về các states mới sau khi thực hiện action đó.
    """
    filtered_states = []
    new_states = []
    transitions = []
    
    # Lọc các states có thể thực hiện action
    for state in belief_state:
        if action in get_valid_moves(state):
            filtered_states.append(state)
            new_state = move(state, action)
            new_states.append(new_state)
            transitions.append((state, action, new_state))
            
    return filtered_states, new_states, transitions

def is_belief_state_goal(belief_state, goal_state):
    """Kiểm tra xem TẤT CẢ các trạng thái trong belief state có phải là goal không"""
    return all(are_states_equal(state, goal_state) for state in belief_state)

def no_observation_search_recursive(belief_state, goal_state, level=0, path=None, visited=None, search_trace=None, max_depth=30):
    """
    Hàm đệ quy tìm kiếm không quan sát với backtracking.
    """
    if path is None:
        path = []
    if visited is None:
        visited = set()
    if search_trace is None:
        search_trace = []

    # Kiểm tra độ sâu tối đa
    if len(path) >= max_depth:
        search_trace.append({
            'step': len(search_trace),
            'level': level,
            'belief_state_before': belief_state,
            'chosen_action': None,
            'belief_state_after': belief_state,
            'explanation': "Đã đạt đến giới hạn độ sâu!",
            'backtrack': True
        })
        return None, search_trace
    
    # Kiểm tra goal
    if is_belief_state_goal(belief_state, goal_state):
        search_trace.append({
            'step': len(search_trace),
            'level': level,
            'belief_state_before': belief_state,
            'chosen_action': None,
            'belief_state_after': belief_state,
            'explanation': "Đã đạt được trạng thái đích!",
            'backtrack': False
        })
        return path, search_trace
        
    # Chuyển belief state thành dạng có thể hash để kiểm tra đã thăm
    belief_tuple = tuple(tuple(tuple(row) for row in state) for state in belief_state)
    if belief_tuple in visited:
        search_trace.append({
            'step': len(search_trace),
            'level': level,
            'belief_state_before': belief_state,
            'chosen_action': None,
            'belief_state_after': belief_state,
            'explanation': "Trạng thái này đã được thăm trước đó!",
            'backtrack': True
        })
        return None, search_trace
        
    visited.add(belief_tuple)
    
    # Thử từng action có thể
    for action in ['up', 'down', 'left', 'right']:
        # Lọc và tạo belief state mới
        filtered_states, new_states, transitions = get_filtered_belief_state(belief_state, action)
        
        # Nếu không có states nào thực hiện được action này
        if not filtered_states:
            continue
            
        # Cập nhật trace khi thử action
        search_trace.append({
            'step': len(search_trace),
            'level': level,
            'belief_state_before': filtered_states,
            'chosen_action': action,
            'belief_state_after': new_states,
            'explanation': f"Thử hành động {action}. Số trạng thái có thể: {len(new_states)}",
            'backtrack': False
        })
        
        # Đệ quy với belief state mới
        result, updated_trace = no_observation_search_recursive(
            new_states, 
            goal_state,
            level + 1,
            path + [action],
            visited,
            search_trace,
            max_depth
        )
        
        # Nếu tìm thấy đường đi
        if result is not None:
            return result, updated_trace
            
        # Nếu không tìm thấy, quay lui và thử action khác
        search_trace.append({
            'step': len(search_trace),
            'level': level,
            'belief_state_before': filtered_states,
            'chosen_action': None,
            'belief_state_after': filtered_states,
            'explanation': f"Quay lui từ hành động {action} và thử hành động khác",
            'backtrack': True
        })
    
    return None, search_trace

def no_observation_search(initial_belief_state, goal_state, max_steps=5):
    """
    Thuật toán tìm kiếm không quan sát cho 8-puzzle
    - Tại mỗi bước, thử lần lượt các actions
    - Với mỗi action, tạo belief state mới từ các states thực hiện được action đó
    - Nếu không tìm thấy giải pháp, quay lui và thử action khác
    """
    search_trace = [{
        'step': 0,
        'level': 0,
        'belief_state_before': initial_belief_state,
        'chosen_action': None,
        'belief_state_after': initial_belief_state,
        'explanation': "Trạng thái niềm tin ban đầu",
        'backtrack': False
    }]
    
    visited = set()
    solution, final_trace = no_observation_search_recursive(
        initial_belief_state,
        goal_state,
        0,
        [],
        visited,
        search_trace,
        max_steps
    )
    
    return solution, final_trace

def no_observation_controller():
    """Controller cho thuật toán tìm kiếm không quan sát"""
    initial_belief_state = [
        [[1, 2, 3],
         [0, 4, 6],
         [7, 5, 8]],
        [[1, 2, 3],
         [4, 0, 6], 
         [7, 5, 8]]
    ]
    
    goal_state = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 0]]
                  
    # Giới hạn số bước tìm kiếm
    max_steps = 5
    
    start_time = time.time()
    try:
        solution, search_trace = no_observation_search(
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

# Export các hàm cần thiết cho partial_observation
__all__ = ['get_valid_actions_for_belief', 'apply_action_to_belief']