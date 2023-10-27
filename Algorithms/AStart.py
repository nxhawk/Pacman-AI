from queue import PriorityQueue

from Utils.utils import find_nearest_food, Manhattan, DDX, isValid


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
