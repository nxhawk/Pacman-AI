from Utils.utils import find_nearest_food, DDX, isValid


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
