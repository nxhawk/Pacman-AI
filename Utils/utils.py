from constants import FOOD, EMPTY, WALL

DDX = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def isValid(_map, row: int, col: int, N: int, M: int) -> bool:
    return 0 < row < N and 0 < col < M and (_map[row][col] == FOOD or _map[row][col] == EMPTY)


def isValid2(_map, row: int, col: int, N: int, M: int) -> bool:
    return 0 < row < N and 0 < col < M and _map[row][col] != WALL


def Manhattan(x1: int, y1: int, x2: int, y2: int) -> float:
    return abs(x1 - x2) + abs(y1 - y2)
