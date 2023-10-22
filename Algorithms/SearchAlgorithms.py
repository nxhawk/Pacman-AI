from Utils.utils import Manhattan, DDX, isValid, isValid2
from constants import FOOD, MONSTER, WALL
from queue import PriorityQueue


def find_nearest_food(_food_Position: list[list[int]], start_row: int, start_col: int):
    food_row, food_col, _id = -1, -1, -1
    for idx in range(len(_food_Position)):
        if food_row == -1:
            _id = idx
            [food_row, food_col] = _food_Position[idx]
        elif Manhattan(food_row, food_col, start_row, start_col) > Manhattan(_food_Position[idx][0],
                                                                             _food_Position[idx][1], start_row,
                                                                             start_col):
            _id = idx
            [food_row, food_col] = _food_Position[idx]

    return [food_row, food_col, _id]


def BFS(_map, _food_Position, start_row, start_col, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = [[[-1, -1] for _ in range(M)] for _ in range(N)]

    [food_row, food_col, _id] = find_nearest_food(_food_Position, start_row, start_col)

    if _id == -1:
        return []

    lt = []
    chk = False
    visited[start_row][start_col] = True
    lt.append([start_row, start_col])
    while len(lt) > 0:
        [row, col] = lt.pop(0)

        if [row, col] == [food_row, food_col]:
            chk = True
            break

        for [d_r, d_c] in DDX:
            new_row, new_col = row + d_r, col + d_c
            if isValid(_map, new_row, new_col, N, M) and not visited[new_row][new_col]:
                visited[new_row][new_col] = True
                lt.append([new_row, new_col])
                trace[new_row][new_col] = [row, col]

    if not chk:
        _food_Position.pop(_id)
        return BFS(_map, _food_Position, start_row, start_col, N, M)

    result = [[food_row, food_col]]
    [row, col] = trace[food_row][food_col]
    while row != -1:
        result.insert(0, [row, col])
        [row, col] = trace[row][col]

    return result


def Deque_DFS(_map, _food_Position, row, col, N, M, visited, trace):
    if visited[row][col]:
        return 0
    visited[row][col] = True
    trace.append([row, col])
    if _map[row][col] == FOOD:
        return 1

    for [d_r, d_c] in DDX:
        new_row, new_col = row + d_r, col + d_c
        if isValid(_map, new_row, new_col, N, M) and not visited[new_row][new_col]:
            res = Deque_DFS(_map, _food_Position, new_row, new_col, N, M, visited, trace)
            if res == 1:
                return 1
            if len(trace) > 0:
                trace.pop(len(trace) - 1)

    return 0


def DFS(_map, _food_Position, start_row, start_col, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = []

    res = Deque_DFS(_map, _food_Position, start_row, start_col, N, M, visited, trace)

    if res == 1:
        return trace

    return []


def AStar(_map, _food_Position, start_row, start_col, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = {}
    cost = {}
    path = []
    queue = PriorityQueue()

    [food_row, food_col, _id] = find_nearest_food(_food_Position, start_row, start_col)

    if _id == -1:
        return []

    start = (start_row, start_col)
    end = (food_row, food_col)

    cost[(start_row, start_col)] = 0
    queue.put((Manhattan(start_row, start_col, food_row, food_col), start))

    while not queue.empty():
        current = queue.get()[1]
        visited[current[0]][current[1]] = True
        if current == end:
            path.append([current[0], current[1]])
            while current != start:
                current = trace[current]
                path.append([current[0], current[1]])
            path.reverse()
            return path

        for [d_r, d_c] in DDX:
            new_row, new_col = current[0] + d_r, current[1] + d_c
            if isValid(_map, new_row, new_col, N, M) and not visited[new_row][new_col]:
                group = (new_row, new_col)
                cost[group] = cost[current] + 1
                queue.put((cost[group] + Manhattan(new_row, new_col, food_row, food_col), group))
                trace[group] = current

    return path


def update_heuristic(_map, start_row, start_col, current_row, current_col, N, M, depth, visited, _type, cost):
    visited.append((current_row, current_col))

    if depth < 0:
        return
    if (start_row, start_col) == (current_row, current_col):
        return

    point = 0
    if _type == FOOD:
        if depth == 2:
            point = 35
        if depth == 1:
            point = 10
        if depth == 0:
            point = 5

    elif _type == MONSTER:
        if depth == 2:
            point = float("-inf")
        if depth == 1:
            point = float("-inf")
        if depth == 0:
            point = -100

    cost[current_row][current_col] += point

    for [d_r, d_c] in DDX:
        new_row, new_col = current_row + d_r, current_col + d_c
        if isValid2(_map, new_row, new_col, N, M) and (new_row, new_col) not in visited:
            update_heuristic(_map, start_row, start_col, new_row, new_col, N, M, depth - 1, visited.copy(), _type, cost)


def calc_heuristic(_map, start_row, start_col, current_row, current_col, N, M, depth, visited, cost, _visited):
    visited.append((current_row, current_col))

    if depth <= 0:
        return

    for [d_r, d_c] in DDX:
        new_row, new_col = current_row + d_r, current_col + d_c
        if isValid2(_map, new_row, new_col, N, M) and (new_row, new_col) not in visited:

            sub_visited = []
            if _map[new_row][new_col] == FOOD:
                update_heuristic(_map, start_row, start_col, new_row, new_col, N, M, 2, sub_visited, FOOD, cost)
            elif _map[new_row][new_col] == MONSTER:
                update_heuristic(_map, start_row, start_col, new_row, new_col, N, M, 2, sub_visited, MONSTER,
                                 cost)

            calc_heuristic(_map, start_row, start_col, new_row, new_col, N, M, depth - 1, visited.copy(), cost,
                           _visited)

    cost[current_row][current_col] -= _visited[current_row][current_col]


def local_search(_map, start_row, start_col, N, M, _visited):
    visited = []
    cost = [[0 for _ in range(M)] for _ in range(N)]

    calc_heuristic(_map, start_row, start_col, start_row, start_col, N, M, 3, visited, cost, _visited)

    max_f = float("-inf")

    result = []
    for [d_r, d_c] in DDX:
        new_row, new_col = start_row + d_r, start_col + d_c
        if cost[new_row][new_col] - _visited[new_row][new_col] > max_f and _map[new_row][new_col] != WALL:
            max_f = cost[new_row][new_col] - _visited[new_row][new_col]
            result = [new_row, new_col]

    return result


def Ghost_move_level4(_map, start_row, start_col, end_row, end_col, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = {}
    cost = {}
    path = []
    queue = PriorityQueue()

    start = (start_row, start_col)
    end = (end_row, end_col)

    cost[(start_row, start_col)] = 0
    queue.put((Manhattan(start_row, start_col, end_row, end_col), start))

    while not queue.empty():
        current = queue.get()[1]
        visited[current[0]][current[1]] = True
        if current == end:
            path.append([current[0], current[1]])
            while current != start:
                current = trace[current]
                path.append([current[0], current[1]])
            path.reverse()
            return path[1] if len(path) > 1 else [start_row, start_col]

        for [d_r, d_c] in DDX:
            new_row, new_col = current[0] + d_r, current[1] + d_c
            if isValid2(_map, new_row, new_col, N, M) and not visited[new_row][new_col]:
                group = (new_row, new_col)
                cost[group] = cost[current] + 1
                queue.put((cost[group] + Manhattan(new_row, new_col, end_row, end_col), group))
                trace[group] = current

    return [start_row, start_col]
