from Utils.utils import DDX, isValid2, isValid
from constants import FOOD, MONSTER


def calc_heuristic(_map, visited, start_row, start_col, new_row, new_col, N, M, depth):
    if abs(start_row - new_row) > 3 or abs(start_col - new_col) > 3 or depth > 9:
        return 0
    if not isValid2(_map, new_row, new_col, N, M):
        return -float("inf")
    if (new_row, new_col) in visited:
        return 0

    visited.append((new_row, new_col))

    score = 0
    if _map[new_row][new_col] == FOOD:
        score = 1000 - depth * 10
    elif _map[new_row][new_col] == MONSTER and depth <= 2:
        return -float("inf")
    else:
        score = 100 - depth * 10

    for [d_r, d_c] in DDX:
        new_row_r, new_col_c = new_row + d_r, new_col + d_c
        if isValid2(_map, new_row_r, new_col_c, N, M):
            score += calc_heuristic(_map.copy(), visited.copy(), start_row, start_col, new_row_r, new_col_c, N, M,
                                    depth + 1)

    return score


def local_search(_map, start_row, start_col, N, M, _visited):
    res = []
    visited = [(start_row, start_col)]
    for [d_r, d_c] in DDX:
        new_row, new_col = start_row + d_r, start_col + d_c
        if isValid(_map, new_row, new_col, N, M):
            res.append(([new_row, new_col], calc_heuristic(_map.copy(), visited.copy(), start_row, start_col, new_row,
                                                           new_col, N, M, 1) - _visited[new_row][new_col]))

    res.sort(key=lambda k: k[1])
    if len(res) > 0:
        return res[-1][0]
    return []
