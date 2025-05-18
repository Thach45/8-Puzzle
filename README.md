# 8-Puzzle Solver Project

## 1. Mục tiêu
Triển khai và so sánh hiệu suất của các thuật toán tìm kiếm khác nhau trong việc giải quyết bài toán 8-puzzle, bao gồm:
- Các thuật toán tìm kiếm không có thông tin
- Các thuật toán tìm kiếm có thông tin
- Các thuật toán tìm kiếm cục bộ
- Các thuật toán tìm kiếm trong môi trường phức tạp
- Các thuật toán tìm kiếm trong môi trường có ràng buộc
- Các thuật toán tìm kiếm tăng cường

## 2. Nội dung

### 2.1 Các thuật toán Tìm kiếm không có thông tin

#### Thành phần chính của bài toán:
- **Trạng thái**: Ma trận 3x3 thể hiện vị trí các số từ 0-8 (0 đại diện cho ô trống)
- **Trạng thái ban đầu**: Cấu hình ban đầu của puzzle
- **Trạng thái đích**: Cấu hình đích cần đạt được
- **Phép di chuyển hợp lệ**: Di chuyển ô trống lên, xuống, trái, phải (nếu có thể)

#### Mô phỏng thuật toán:
```
[Hình GIF minh họa quá trình giải của BFS]
Mô tả: Thuật toán BFS tìm kiếm theo chiều rộng, khám phá tất cả các trạng thái ở cùng độ sâu trước khi đi sâu hơn.

[Hình GIF minh họa quá trình giải của DFS]
Mô tả: Thuật toán DFS đi sâu theo một nhánh cho đến khi không thể đi tiếp hoặc tìm thấy đích.

[Hình GIF minh họa quá trình giải của UCS]
Mô tả: UCS mở rộng theo chi phí đường đi, đảm bảo tìm được đường đi tối ưu.

[Hình GIF minh họa quá trình giải của IDDFS]
Mô tả: IDDFS kết hợp chiến lược của DFS với giới hạn độ sâu tăng dần.
```

#### So sánh hiệu suất:
```
[Biểu đồ so sánh thời gian thực thi]
[Biểu đồ so sánh bộ nhớ sử dụng]
[Biểu đồ so sánh số trạng thái đã duyệt]
```

#### Nhận xét:
- BFS có ưu điểm là luôn tìm được đường đi ngắn nhất, nhưng nhược điểm là tốn nhiều bộ nhớ
- DFS ít tốn bộ nhớ hơn nhưng không đảm bảo tìm được đường đi ngắn nhất
- UCS phù hợp khi chi phí các bước di chuyển khác nhau
- IDDFS là sự lựa chọn tốt khi cần cân bằng giữa tối ưu và bộ nhớ

### 2.2 Các thuật toán Tìm kiếm có thông tin

#### Mô phỏng thuật toán:
```
[Hình GIF minh họa Greedy Best-First Search]
Mô tả: Thuật toán luôn chọn trạng thái có heuristic tốt nhất.

[Hình GIF minh họa A* Search]
Mô tả: A* kết hợp chi phí thực tế và heuristic để tìm đường đi tối ưu.

[Hình GIF minh họa IDA* Search]
Mô tả: IDA* thực hiện tìm kiếm theo độ sâu với giới hạn dựa trên f-value.

[Hình GIF minh họa Beam Search]
Mô tả: Beam Search giới hạn số lượng trạng thái xét ở mỗi bước.
```

#### So sánh hiệu suất:
```
[Biểu đồ so sánh các thuật toán informed search]
[Biểu đồ đánh giá chất lượng lời giải]
```

#### Nhận xét:
- Greedy Best-First Search nhanh nhưng không đảm bảo tối ưu
- A* cân bằng tốt giữa tốc độ và chất lượng lời giải
- IDA* hiệu quả về mặt bộ nhớ cho không gian trạng thái lớn
- Beam Search là lựa chọn tốt khi cần giải pháp nhanh và chấp nhận được gần đúng

### 2.3 Các thuật toán tìm kiếm cục bộ

#### Mô phỏng thuật toán:
```
[Hình GIF minh họa Hill Climbing]
[Hình GIF minh họa Simulated Annealing]
```

#### So sánh hiệu suất:
```
[Biểu đồ so sánh tốc độ hội tụ]
[Biểu đồ khả năng thoát cực trị địa phương]
```

#### Nhận xét:
- Hill Climbing đơn giản và nhanh nhưng dễ bị mắc kẹt
- Simulated Annealing hiệu quả trong việc tránh cực trị địa phương
- Stochastic Hill Climbing cân bằng giữa khám phá và khai thác
- Local search thích hợp khi không cần đường đi tối ưu

### 2.4 Các thuật toán tìm kiếm trong môi trường phức tạp

#### Tìm kiếm không quan sát (No Observation Search):
- Thực hiện tìm kiếm khi không có thông tin về trạng thái hiện tại
- Sử dụng belief state để theo dõi tập các trạng thái có thể
- Cập nhật belief state dựa trên các hành động đã thực hiện

```
[Hình GIF minh họa No Observation Search]
Mô tả: Thuật toán hoạt động trong điều kiện không có thông tin về trạng thái
```

#### Tìm kiếm quan sát một phần (Partial Observation Search):
- Kết hợp thông tin quan sát được với belief state
- Cập nhật belief state dựa trên cả hành động và quan sát
- Sử dụng chiến lược information gathering khi cần thiết

```
[Hình GIF minh họa Partial Observation Search]
Mô tả: Thuật toán sử dụng thông tin quan sát một phần để cải thiện quá trình tìm kiếm
```

#### AND-OR Search:
- Xử lý các trường hợp không gian trạng thái phức tạp
- Phân tích cả thành công và thất bại của các nhánh

#### Nhận xét:
- No Observation Search phù hợp với môi trường hoàn toàn không biết trước
- Partial Observation Search cân bằng giữa thu thập thông tin và tối ưu hóa
- AND-OR Search hiệu quả cho các bài toán có nhiều nhánh quyết định

### 2.5 Các thuật toán tìm kiếm trong môi trường có ràng buộc

#### Mô phỏng thuật toán:
```
[Hình GIF minh họa Forward Checking]
[Hình GIF minh họa AC-3]
[Hình GIF minh họa Backtracking]
```

#### So sánh hiệu suất:
```
[Biểu đồ so sánh tốc độ giải quyết ràng buộc]
```

#### Nhận xét:
- Forward Checking giảm không gian tìm kiếm bằng cách kiểm tra sớm
- AC-3 hiệu quả trong việc duy trì tính nhất quán cục bộ
- Backtracking đơn giản nhưng có thể chậm với bài toán phức tạp

### 2.6 Các thuật toán tìm kiếm tăng cường

#### Mô phỏng Q-Learning:
```
[Hình GIF minh họa quá trình học Q-Learning]
[Biểu đồ hội tụ của Q-values]
```

#### Nhận xét:
- Q-Learning hiệu quả trong việc học từ trải nghiệm
- Cần thời gian để hội tụ nhưng cho kết quả tốt
- Phù hợp cho các bài toán có không gian trạng thái lớn

## 3. Kết luận

### Nhận xét tổng quan về các nhóm thuật toán:

1. **Tìm kiếm không có thông tin**:
   - Phù hợp khi không có thông tin heuristic
   - BFS và IDDFS là lựa chọn tốt nhất trong nhóm
   - Cần cân nhắc giữa tối ưu và bộ nhớ

2. **Tìm kiếm có thông tin**:
   - Hiệu quả hơn nhờ sử dụng heuristic
   - A* là thuật toán toàn diện nhất
   - Beam Search tốt cho ứng dụng thời gian thực

3. **Tìm kiếm cục bộ**:
   - Nhanh và ít tốn bộ nhớ
   - Simulated Annealing là lựa chọn cân bằng nhất
   - Thích hợp cho bài toán tối ưu hóa

4. **Tìm kiếm trong môi trường phức tạp**:
   - Xử lý tốt môi trường không chắc chắn
   - Partial Observation hiệu quả hơn No Observation
   - Cần chiến lược thu thập thông tin phù hợp

5. **Tìm kiếm có ràng buộc**:
   - Forward Checking và AC-3 hiệu quả cho CSP
   - Cần kết hợp nhiều kỹ thuật để tối ưu
   - Phù hợp cho bài toán lập lịch, quy hoạch

6. **Tìm kiếm tăng cường**:
   - Học từ tương tác với môi trường
   - Hiệu quả cho bài toán dài hạn
   - Cần thời gian huấn luyện

### Kết quả đạt được:
1. Triển khai thành công 6 nhóm thuật toán tìm kiếm
2. Xây dựng hệ thống mô phỏng trực quan
3. Phân tích hiệu suất chi tiết
4. Đề xuất các trường hợp sử dụng phù hợp

### Đề xuất cải tiến:
1. Tối ưu hóa hiệu suất các thuật toán
2. Thêm các heuristic khác để so sánh
3. Mở rộng cho bài toán N-puzzle
4. Cải thiện giao diện người dùng