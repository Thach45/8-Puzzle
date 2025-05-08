import copy
from collections import defaultdict

# Định nghĩa trạng thái 8-puzzle (dùng tuple để dễ so sánh)
class PuzzleState:
    def __init__(self, board):
        self.board = tuple(tuple(row) for row in board)  # Chuyển thành tuple để hash
        self.size = len(board)
    
    def get_blank_pos(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        return hash(self.board)
    
    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.board])

# Định nghĩa bài toán 8-puzzle
class PuzzleProblem:
    def __init__(self, initial_states, goal_state):
        self.initial_belief_state = set(initial_states)  # Trạng thái niềm tin ban đầu
        self.goal_state = goal_state
    
    def actions(self, state):
        """Trả về các hành động khả thi từ trạng thái."""
        blank_pos = state.get_blank_pos()
        i, j = blank_pos
        possible_actions = []
        if i > 0:
            possible_actions.append('Up')
        if i < state.size - 1:
            possible_actions.append('Down')
        if j > 0:
            possible_actions.append('Left')
        if j < state.size - 1:
            possible_actions.append('Right')
        return possible_actions
    
    def result(self, state, action):
        """Trả về trạng thái mới sau khi thực hiện hành động."""
        blank_pos = state.get_blank_pos()
        i, j = blank_pos
        new_board = [list(row) for row in state.board]
        
        if action == 'Up':
            new_board[i][j], new_board[i-1][j] = new_board[i-1][j], new_board[i][j]
        elif action == 'Down':
            new_board[i][j], new_board[i+1][j] = new_board[i+1][j], new_board[i][j]
        elif action == 'Left':
            new_board[i][j], new_board[i][j-1] = new_board[i][j-1], new_board[i][j]
        elif action == 'Right':
            new_board[i][j], new_board[i][j+1] = new_board[i][j+1], new_board[i][j]
        
        return PuzzleState(new_board)
    
    def goal_test(self, belief_state):
        """Kiểm tra xem tất cả trạng thái trong trạng thái niềm tin có phải là mục tiêu."""
        return all(state.board == self.goal_state.board for state in belief_state)
    
    def percept(self, state):
        """Quan sát: trả về vị trí của ô trống."""
        return state.get_blank_pos()
    
    def predict(self, belief_state, action):
        """Dự đoán: áp dụng hành động lên tất cả trạng thái hợp lệ trong trạng thái niềm tin."""
        new_belief_state = set()
        for state in belief_state:
            if action in self.actions(state):
                new_state = self.result(state, action)
                new_belief_state.add(new_state)
        return new_belief_state
    
    def possible_percepts(self, belief_state):
        """Dự đoán quan sát: trả về tập hợp các quan sát có thể từ trạng thái niềm tin."""
        return {self.percept(state) for state in belief_state}
    
    def update(self, belief_state, percept):
        """Cập nhật: giữ lại các trạng thái tương thích với quan sát."""
        return {state for state in belief_state if self.percept(state) == percept}

# Thuật toán AND-OR search cho tìm kiếm với quan sát một phần
def and_or_graph_search(problem):
    """Triển khai AND-OR search để tìm kế hoạch dự phòng."""
    def or_search(belief_state, problem, path):
        if problem.goal_test(belief_state):
            return []  # Kế hoạch rỗng nếu đạt mục tiêu
        
        # Kiểm tra lặp (cycle detection)
        belief_state_tuple = tuple(sorted(hash(s) for s in belief_state))
        if belief_state_tuple in path:
            return None  # Thất bại nếu lặp
        
        # Thử từng hành động
        for action in {'Up', 'Down', 'Left', 'Right'}:  # Giả sử tất cả hành động có thể
            predicted_belief = problem.predict(belief_state, action)
            if not predicted_belief:  # Nếu không có trạng thái nào hợp lệ với hành động
                continue
            
            # Dự đoán quan sát
            percepts = problem.possible_percepts(predicted_belief)
            conditional_plan = []
            
            # Xử lý từng quan sát
            for percept in percepts:
                new_belief_state = problem.update(predicted_belief, percept)
                if not new_belief_state:  # Nếu trạng thái niềm tin rỗng
                    continue
                
                # Gọi đệ quy AND-SEARCH
                plan = and_search(new_belief_state, problem, path | {belief_state_tuple})
                if plan is not None:
                    conditional_plan.append((percept, plan))
                else:
                    break  # Nếu một nhánh thất bại, toàn bộ AND node thất bại
            
            # Nếu tất cả nhánh trong AND node thành công
            if len(conditional_plan) == len(percepts) and conditional_plan:
                return [action] + [f"if percept={percept} then {plan}" for percept, plan in conditional_plan]
        
        return None  # Thất bại nếu không hành động nào thành công
    
    def and_search(belief_state, problem, path):
        """Xử lý AND node: tìm kế hoạch cho tất cả trạng thái niềm tin từ các quan sát."""
        return or_search(belief_state, problem, path)
    
    # Bắt đầu tìm kiếm từ trạng thái niềm tin ban đầu
    return or_search(problem.initial_belief_state, problem, set())

# Ví dụ chạy
def main():
    # Trạng thái mục tiêu
    goal_board = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8]
    ]
    goal_state = PuzzleState(goal_board)
    
    # Trạng thái niềm tin ban đầu (2 trạng thái)
    initial_board_1 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    initial_board_2 = [
        [1, 2, 3],
        [4, 5, 0],
        [7, 8, 6]
    ]
    initial_states = {PuzzleState(initial_board_1), PuzzleState(initial_board_2)}
    
    # Khởi tạo bài toán
    problem = PuzzleProblem(initial_states, goal_state)
    
    # Chạy AND-OR search
    plan = and_or_graph_search(problem)
    
    # In kết quả
    if plan:
        print("Kế hoạch dự phòng:")
        for step in plan:
            print(step)
    else:
        print("Không tìm thấy kế hoạch!")

if __name__ == "__main__":
    main()