# Pacman AI - PROJECT 01: SEARCH - HCMUS

  <img align="right" width="100%" src="https://github.com/nxhawk/PacMan_AI/assets/92797788/9d0bba9d-4ddc-47ec-9d5b-f8059fcc71aa">



You are given a file that describes Pac-man World. Suggest or implement learned
algorithms to assist Pac-Man in finding food without getting killed by monsters.
In the game Pac-Man, both Pac-Man and the monsters are constrained to moving in four
directions: left, right, up, and down. They are not able to move through walls. The game is
divided into four distinct levels, and each level has its own set of rules.
* Level 1: Pac-Man is aware of the food's position on the map, and there are no
monsters present. There is only one food item on the map.
* Level 2: Monsters are stationary and do not move around. If Pac-Man and a monster
collide with each other, the game ends. There is still one food item on the map, and
Pac-Man knows its position.
* Level 3: Pac-Man's visibility is limited to its nearest three steps. Foods outside this
range are not visible to Pac-Man. Pac-Man can only scan the adjacent tiles within
the 8 tiles x 3 range. There are multiple food items spread throughout the map.
Monsters can move one step in any valid direction around their initial location at
the start of the game. Both Pac-Man and monsters move one step per turn.
* Level 4 (difficult) involves an enclosed map where monsters relentlessly pursue
Pac-Man. Pac-Man must gather as much food as possible while avoiding being
overtaken by any monster. The monsters have the ability to pass through each other.
Both Pac-Man and the monsters move one step per turn, and the map contains a
multitude of food items.

The calculation of game points follows these rules:
- Each movement deducts 1 point from your score.
- Collecting each food item awards you 20 points.

To comprehensively compare the performance of different algorithms, it is recommended
to run them on various graphs and evaluate them based on the following aspects:
- Time is taken to complete the task.
- Length of the discovered paths.
  
It is particularly important to generate challenging maps, such as placing Pac-Man between
two monsters or creating a scenario where walls surround Pac-Man on all sides. This will
test the algorithms' abilities to handle difficult situations.

## Mô tả

| STT | Yêu cầu | Thực hiện | Hoàn thành |
| ------ | ------ | ----- | ----- |
| 1 | Level 1: Pacman biết vị trí của thức ăn trong bản đồ, không có Monster. Chỉ có một thức ăn tồn tại trên bản đồ | Sử dụng thuật toán Breadth-first search để tìm đường đi ngắn nhất đến thức ăn. | 100% |
| 2 | Level 2: Monster không thể di chuyển, nếu Pacman và Monster va chạm thì trò chơi kết thúc. Vẫn chỉ có một thức ăn tồn tại trên bản đồ và Pacman biết vị trí của nó. | Sử dụng thuật toán Breadth-first search để tìm đường đi ngắn nhất đến thức ăn. | 100% |
| 3 | Level 3: Tầm nhìn của Pacman bị giới hạn chỉ còn 3 đơn vị. Tức Pacman chỉ có thể “nhìn thấy” phạm vi 8 đơn vị xung quanh và mở rộng ra 3 đơn vị. Có nhiều thức ăn tồn tại trên bản đồ. Monster di chuyển từng bước một xung quanh vị trí bắt đầu. Với mỗi bước Pacman di chuyển, Monster cũng di chuyển. | Sử dụng thuật toán heuristic local search để tìm đường đi cho Pacman. | 100% |
| 4 | Level 4: Bản đồ kín. Monster sẽ truy đuổi nhằm tiêu diệt Pacman. Pacman sẽ cố gắng ăn nhiều thức ăn nhất có thể. Pacman sẽ thua cuộc nếu va chạm phải Monster. Monster có thể đi xuyên qua nhau. Với mỗi bước Pacman di chuyển, Monster cũng di chuyển. Có rất nhiều thức ăn. | Sử dụng thuật toán minimax để tìm đường đi cho Pacman. Sử dụng thuật toán A* để di chuyển Monster. | 100% |
| 5 | Biểu diễn đồ họa mỗi bước. | Sử dụng Pygame | 100% |
| 6 | Tạo ít nhất 5 bản đồ với tường, Monster và thức ăn khác nhau. | | 100% |
| 7 | Báo cáo thuật toán | | 100% |

## How to run

`Bước 1:` Run command line `git clone https://github.com/nxhawk/Pacman-AI-HCMUS.git`

`Bước 2:` Bật console <b>cùng cấp</b> với file `main.py` (trong thư mục <b>Source</b>).

`Bước 3:` Nếu đã cài đặt python và pygame thì bỏ qua bước này. 
Cài đặt Python trên trang chủ [python.org](https://www.python.org/downloads/). 
Nếu chưa cài đặt pygame thì có thể dùng command line thực thi lệnh sau: `pip install pygame` hoặc `pip install –r requirements.txt`.

`Bước 4:` Để chạy chương trình dùng lệnh `py main.py` hoặc `python main.py`. 

Trong trường hợp bạn dùng pycharm có thể mở thư mục chứa folder <b>Source</b> và <b>Input</b> rồi chạy file `main.py`.

## Tài liệu tham khảo

- [UC-Berkeley-AI-Pacman-Project](https://github.com/karlapalem/UC-Berkeley-AI-Pacman-Project)
- [Pygame docs](https://www.pygame.org/docs/)

