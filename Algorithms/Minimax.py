from Utils.utils import Manhattan, DDX, isValid2, isValid
from constants import FOOD, MONSTER, EMPTY

_food_pos = []


def evaluationFunction(_map, pac_row, pac_col, N, M, score):
    # get food position
    ghost_pos = []
    distancesToFoodList = []
    for row in range(N):
        for col in range(M):
            if _map[row][col] == FOOD:
                distancesToFoodList.append(Manhattan(row, col, pac_row, pac_col))
            if _map[row][col] == MONSTER:
                ghost_pos.append([row, col])
            if _map[row][col] == EMPTY:
                score += 5

    # Consts
    INF = 100000000.0  # Infinite value
    WEIGHT_FOOD = 100.0  # Food base value
    WEIGHT_GHOST = -150.0  # Ghost base value

    _score = score
    if len(distancesToFoodList) > 0:
        _score += WEIGHT_FOOD / (min(distancesToFoodList) if min(distancesToFoodList) != 0 else 1)
    else:
        _score += WEIGHT_FOOD

    for [g_r, g_c] in ghost_pos:
        distance = Manhattan(pac_row, pac_col, g_r, g_c)
        if distance > 0:
            _score += WEIGHT_GHOST / distance
        else:
            return -INF

    return _score


def minimaxAgent(_map, pac_row, pac_col, N, M, depth, Score):
    def terminal(_map, _pac_row, _pac_col, _N, _M, _depth) -> bool:
        if _map[_pac_row][_pac_col] == MONSTER or _depth == 0:
            return True

        for row in range(_N):
            for col in range(_M):
                if _map[row][col] == FOOD:
                    return False

        return True

    def min_value(_map, _pac_row, _pac_col, _N, _M, _depth, score):
        if terminal(_map, _pac_row, _pac_col, _N, _M, _depth):
            return evaluationFunction(_map, _pac_row, _pac_col, _N, _M, score)

        v = 10000000000000000
        for row in range(_N):
            for col in range(_M):
                if _map[row][col] == MONSTER:
                    for [_d_r, _d_c] in DDX:
                        _new_r, _new_c = _d_r + row, _d_c + col
                        if isValid2(_map, _new_r, _new_c, _N, _M):
                            state = _map[_new_r][_new_c]
                            _map[_new_r][_new_c] = MONSTER
                            _map[row][col] = EMPTY
                            v = min(v, max_value(_map, _pac_row, _pac_col, _N, _M, _depth - 1, score))
                            _map[_new_r][_new_c] = state
                            _map[row][col] = MONSTER
        return v

    def max_value(_map, _pac_row, _pac_col, _N, _M, _depth, score):
        if terminal(_map, _pac_row, _pac_col, _N, _M, _depth):
            return evaluationFunction(_map, _pac_row, _pac_col, _N, _M, score)

        v = -10000000000000000
        for [_d_r, _d_c] in DDX:
            _new_r, _new_c = _pac_row + _d_r, _pac_col + _d_c
            if isValid(_map, _new_r, _new_c, _N, _M):
                state = _map[_new_r][_new_c]
                _map[_new_r][_new_c] = EMPTY
                if state == FOOD:
                    score += 20
                    _food_pos.pop(_food_pos.index((_new_r, _new_c)))
                else:
                    score -= 1
                v = max(v, min_value(_map, _new_r, _new_c, _N, _M, _depth - 1, score))
                _map[_new_r][_new_c] = state
                if state == FOOD:
                    score -= 20
                    _food_pos.append((_new_r, _new_c))
                else:
                    score += 1
        return v

    res = []
    global _food_pos
    _food_pos = []
    for _row in range(N):
        for _col in range(M):
            if _map[_row][_col] == FOOD:
                _food_pos.append((_row, _col))

    for [d_r, d_c] in DDX:
        new_r, new_c = pac_row + d_r, pac_col + d_c
        if isValid(_map, new_r, new_c, N, M):
            _state = _map[new_r][new_c]
            _map[new_r][new_c] = EMPTY
            if _state == FOOD:
                Score += 20
                _food_pos.pop(_food_pos.index((new_r, new_c)))
            else:
                Score -= 1
            res.append(([new_r, new_c], min_value(_map, new_r, new_c, N, M, depth, Score)))
            _map[new_r][new_c] = _state
            if _state == FOOD:
                Score -= 20
                _food_pos.append((new_r, new_c))
            else:
                Score += 1

    res.sort(key=lambda k: k[1])
    if len(res) > 0:
        return res[-1][0]
    return []
