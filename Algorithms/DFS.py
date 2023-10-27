from Utils.utils import DDX, isValid
from constants import FOOD


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
