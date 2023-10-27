from constants import FOOD, EMPTY, WALL

DDX = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def isValid(_map, row: int, col: int, N: int, M: int) -> bool:
    return 0 < row < N and 0 < col < M and (_map[row][col] == FOOD or _map[row][col] == EMPTY)


def isValid2(_map, row: int, col: int, N: int, M: int) -> bool:
    return 0 < row < N and 0 < col < M and _map[row][col] != WALL


def Manhattan(x1: int, y1: int, x2: int, y2: int) -> float:
    return abs(x1 - x2) + abs(y1 - y2)


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
