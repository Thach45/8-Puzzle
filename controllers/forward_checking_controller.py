from typing import List, Tuple, Set, Dict
from collections import defaultdict

class ForwardCheckingController:
    def __init__(self):
        # Goal state cố định
        self.goal_state = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 0: (2, 2)
        }
        
    def get_initial_domains(self) -> Dict[Tuple[int, int], Set[int]]:
        """Khởi tạo miền giá trị cho mỗi biến (vị trí)"""
        domains = {}
        for i in range(3):
            for j in range(3):
                if (i, j) == (2, 2):  # Vị trí của ô trống
                    domains[(i, j)] = {0}
                else:
                    domains[(i, j)] = set(range(1, 9))  # Các số từ 1-8
        return domains

    def check_constraints(self, assignment: Dict[Tuple[int, int], int], var: Tuple[int, int], value: int) -> bool:
        """Kiểm tra ràng buộc cho một giá trị được gán"""
        # Kiểm tra xem giá trị đã được sử dụng chưa
        for pos, val in assignment.items():
            if pos != var and val == value:
                return False
        
        # Kiểm tra xem vị trí có phù hợp với goal state không
        if value != 0:  # Bỏ qua ô trống
            goal_pos = self.goal_state[value]
            if var == goal_pos:
                return True
            # Cho phép một số linh hoạt trong việc đặt số
            manhattan_dist = abs(var[0] - goal_pos[0]) + abs(var[1] - goal_pos[1])
            if manhattan_dist > 2:  # Không cho phép đặt quá xa vị trí mục tiêu
                return False
        
        return True

    def forward_checking(self, var: Tuple[int, int], value: int, domains: Dict[Tuple[int, int], Set[int]], 
                        assignment: Dict[Tuple[int, int], int]) -> Dict[Tuple[int, int], Set[int]]:
        """Thực hiện forward checking sau khi gán giá trị"""
        new_domains = {k: v.copy() for k, v in domains.items()}
        
        # Loại bỏ giá trị đã sử dụng khỏi domain của các biến chưa gán
        for other_var in domains:
            if other_var not in assignment and other_var != var:
                if value in new_domains[other_var]:
                    new_domains[other_var].remove(value)
                    if not new_domains[other_var]:  # Domain trống
                        return None
        
        return new_domains

    def solve(self) -> List[Dict[Tuple[int, int], int]]:
        """Giải bài toán sử dụng Forward Checking"""
        # Khởi tạo miền giá trị và assignment
        domains = self.get_initial_domains()
        assignment = {}
        solution_steps = []
        
        def backtrack() -> bool:
            if len(assignment) == 9:  # Đã gán hết các ô
                return True
            
            # Chọn biến chưa gán tiếp theo
            unassigned = [(i, j) for i in range(3) for j in range(3) if (i, j) not in assignment]
            if not unassigned:
                return True
                
            var = min(unassigned, key=lambda pos: len(domains[pos]))
            
            # Thử các giá trị từ domain
            for value in sorted(domains[var]):
                if self.check_constraints(assignment, var, value):
                    # Lưu domain hiện tại để có thể khôi phục
                    old_domains = {k: v.copy() for k, v in domains.items()}
                    
                    # Forward checking
                    assignment[var] = value
                    new_domains = self.forward_checking(var, value, domains, assignment)
                    
                    if new_domains is not None:
                        # Cập nhật domains và lưu bước giải
                        domains.update(new_domains)
                        current_state = self.get_current_state(assignment)
                        solution_steps.append(current_state)
                        
                        if backtrack():
                            return True
                    
                    # Quay lui
                    del assignment[var]
                    domains.update(old_domains)
                    if solution_steps:
                        solution_steps.pop()
            
            return False
        
        if backtrack():
            return solution_steps
        return []

    def get_current_state(self, assignment: Dict[Tuple[int, int], int]) -> List[List[int]]:
        """Chuyển đổi assignment thành trạng thái dạng ma trận"""
        state = [[0] * 3 for _ in range(3)]
        for (i, j), value in assignment.items():
            state[i][j] = value
        return state

    def render_template(self):
        """Render template với kết quả giải"""
        from flask import render_template
        
        solution_path = self.solve()
        initial_state = [[0] * 3 for _ in range(3)]  # Trạng thái ban đầu trống
        
        return render_template('forward_checking.html',
                           initial_state=initial_state,
                           solution_path=solution_path,
                           visited_states=len(solution_path))

def forward_checking_controller():
    controller = ForwardCheckingController()
    return controller.render_template()