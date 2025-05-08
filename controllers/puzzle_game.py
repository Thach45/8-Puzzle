from typing import List, Tuple, Dict, Set
import random
import copy

class PuzzleState:
    def __init__(self, board: List[List[int]]):
        self.board = board
        self.size = len(board)
        
    def get_blank_pos(self) -> Tuple[int, int]:
        """Tìm vị trí ô trống (số 0)"""
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return (i, j)
        raise ValueError("Không tìm thấy ô trống")

    def get_valid_moves(self) -> List[str]:
        """Lấy danh sách các nước đi hợp lệ"""
        moves = []
        i, j = self.get_blank_pos()
        
        if i > 0: moves.append('up')
        if i < self.size - 1: moves.append('down') 
        if j > 0: moves.append('left')
        if j < self.size - 1: moves.append('right')
        
        return moves

    def apply_move(self, move: str) -> 'PuzzleState':
        """Thực hiện một nước đi và trả về trạng thái mới"""
        if move not in self.get_valid_moves():
            raise ValueError(f"Nước đi không hợp lệ: {move}")
            
        new_board = [row[:] for row in self.board]
        i, j = self.get_blank_pos()
        
        if move == 'up':
            new_board[i][j], new_board[i-1][j] = new_board[i-1][j], new_board[i][j]
        elif move == 'down':
            new_board[i][j], new_board[i+1][j] = new_board[i+1][j], new_board[i][j]
        elif move == 'left':  
            new_board[i][j], new_board[i][j-1] = new_board[i][j-1], new_board[i][j]
        elif move == 'right':
            new_board[i][j], new_board[i][j+1] = new_board[i][j+1], new_board[i][j]
            
        return PuzzleState(new_board)

    def get_manhattan_distance(self, goal_state: 'PuzzleState') -> int:
        """Tính khoảng cách Manhattan đến trạng thái đích"""
        distance = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    # Tìm vị trí đích của số hiện tại
                    for x in range(self.size):
                        for y in range(self.size):
                            if goal_state.board[x][y] == self.board[i][j]:
                                distance += abs(i - x) + abs(j - y)
                                break
        return distance

    def is_goal(self, goal_state: 'PuzzleState') -> bool:
        """Kiểm tra xem có phải trạng thái đích không"""
        return all(self.board[i][j] == goal_state.board[i][j] 
                  for i in range(self.size) 
                  for j in range(self.size))

    def __eq__(self, other: 'PuzzleState') -> bool:
        return isinstance(other, PuzzleState) and self.board == other.board

    def __hash__(self) -> int:
        return hash(str(self.board))

    def __str__(self) -> str:
        return '\n'.join([' '.join(map(str, row)) for row in self.board])

class ObservationModel:
    """Lớp cơ sở cho các mô hình quan sát"""
    def get_observation(self, state: PuzzleState) -> Dict:
        raise NotImplementedError()

class FullObservation(ObservationModel):
    """Quan sát đầy đủ - nhìn thấy toàn bộ trạng thái"""
    def get_observation(self, state: PuzzleState) -> Dict:
        return {
            'type': 'full',
            'board': copy.deepcopy(state.board)
        }

class PartialObservation(ObservationModel):
    """Quan sát một phần - chỉ nhìn thấy các ô xung quanh ô trống"""
    def get_observation(self, state: PuzzleState) -> Dict:
        blank_i, blank_j = state.get_blank_pos()
        visible = set()  # Các ô có thể nhìn thấy
        
        # Thêm ô trống và các ô lân cận
        for di, dj in [(0,0), (-1,0), (1,0), (0,-1), (0,1)]:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < state.size and 0 <= new_j < state.size:
                visible.add((new_i, new_j))
        
        # Tạo bảng quan sát với chỉ các ô visible
        obs_board = [[None]*state.size for _ in range(state.size)]
        for i, j in visible:
            obs_board[i][j] = state.board[i][j]
            
        return {
            'type': 'partial',
            'board': obs_board,
            'visible_cells': list(visible)
        }

class NoObservation(ObservationModel):
    """Không quan sát - chỉ biết các nước đi hợp lệ"""
    def get_observation(self, state: PuzzleState) -> Dict:
        return {
            'type': 'no',
            'valid_moves': state.get_valid_moves()
        }

def create_random_puzzle() -> PuzzleState:
    """Tạo một câu đố 8-puzzle ngẫu nhiên có thể giải được"""
    goal = [[1,2,3], [4,5,6], [7,8,0]]
    current = PuzzleState(copy.deepcopy(goal))
    
    # Thực hiện 100 bước đi ngẫu nhiên
    for _ in range(100):
        moves = current.get_valid_moves()
        move = random.choice(moves)
        current = current.apply_move(move)
        
    return current 