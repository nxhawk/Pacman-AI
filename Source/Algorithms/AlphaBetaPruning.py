from Utils.utils import Manhattan, DDX, isValid, isValid2
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

    # Consts
    INF = 100000000.0  # Infinite value
    WEIGHT_FOOD = 5.0  # Food base value
    WEIGHT_GHOST = -10.0  # Ghost base value

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


def AlphaBetaAgent(_map, pac_row, pac_col, N, M, depth, Score):
    def terminal(_map, _pac_row, _pac_col, _N, _M, _depth) -> bool:
        if _map[_pac_row][_pac_col] == MONSTER or _depth == 0:
            return True

        for row in range(_N):
            for col in range(_M):
                if _map[row][col] == FOOD:
                    return False

        return True

    def alphabeta(_map, _ghost, _pac_row, _pac_col, _N, _M, _depth, score, alpha, beta, agent):
        if terminal(_map, _pac_row, _pac_col, _N, _M, _depth):
            return evaluationFunction(_map, _pac_row, _pac_col, _N, _M, score)

        if agent == -1:
            v = float("-inf")
        else:
            v = float("inf")

        if agent == -1:  # pacman move
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
                    v = max(v,
                            alphabeta(_map, _ghost, _new_r, _new_c, _N, _M, _depth, score, alpha, beta, 0))
                    _map[_new_r][_new_c] = state
                    if state == FOOD:
                        score -= 20
                        _food_pos.append((_new_r, _new_c))
                    else:
                        score += 1
                    alpha = max(alpha, v)
                    if beta <= alpha:  # alpha-beta pruning
                        break
            return v
        nextAgent = agent + 1
        if nextAgent == len(_ghost):
            nextAgent = -1

        if nextAgent == -1:
            _depth -= 1

        [g_r, g_c] = _ghost[agent]
        for [_d_r, _d_c] in DDX:
            _new_r, _new_c = g_r + _d_r, g_c + _d_c
            if isValid2(_map, _new_r, _new_c, _N, _M):
                state = _map[_new_r][_new_c]
                _map[_new_r][_new_c] = MONSTER
                _map[g_r][g_c] = EMPTY
                _ghost[agent][0], _ghost[agent][1] = _new_r, _new_c
                v = min(v, alphabeta(_map, _ghost, _pac_row, _pac_col, _N, _M, _depth, score, alpha, beta,
                                     nextAgent))
                _ghost[agent][0], _ghost[agent][1] = g_r, g_c
                _map[_new_r][_new_c] = state
                _map[g_r][g_c] = MONSTER
                beta = min(beta, v)
                if beta <= alpha:  # alpha-beta pruning
                    break
        return v

    res = []
    _alpha = float("-inf")
    _beta = float("inf")
    global _food_pos
    _food_pos = []
    _ghost = []
    for _row in range(N):
        for _col in range(M):
            if _map[_row][_col] == FOOD:
                _food_pos.append((_row, _col))
            if _map[_row][_col] == MONSTER:
                _ghost.append([_row, _col])

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
            res.append(([new_r, new_c], alphabeta(_map, _ghost, new_r, new_c, N, M, depth, Score, _alpha, _beta, -1)
                        ))
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
