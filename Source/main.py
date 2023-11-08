import sys

import pygame
import random

from Algorithms.Ghost_Move import Ghost_move_level4
from Algorithms.SearchAgent import SearchAgent
from Object.Food import Food
from Object.Player import Player
from Object.Wall import Wall
from Utils.utils import DDX, isValid2
from constants import *
from Object.Menu import Menu, Button

N = M = Score = _state_PacMan = 0
_map = []
_wall = []
_road = []
_food = []
_ghost = []
_food_Position = []
_ghost_Position = []
_visited = []
PacMan: Player
Level = 1
Map_name = ""

# Initial Pygame --------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PacMan')
clock = pygame.time.Clock()

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
my_font_2 = pygame.font.SysFont('Comic Sans MS', 100)


# ------------------------------------------

def readMapInFile(map_name: str):
    f = open(map_name, "r")
    x = f.readline().split()
    global N, M, _map
    _map = []
    N, M = int(x[0]), int(x[1])
    for _ in range(N):
        line = f.readline().split()
        _m = []
        for j in range(M):
            _m.append(int(line[j]))
        _map.append(_m)

    global PacMan
    x = f.readline().split()

    MARGIN["TOP"] = max(0, (HEIGHT - N * SIZE_WALL) // 2)
    MARGIN["LEFT"] = max(0, (WIDTH - M * SIZE_WALL) // 2)
    PacMan = Player(int(x[0]), int(x[1]), IMAGE_PACMAN[0])

    f.close()


# --------------------------------- MAIN ---------------------

def check_Object(_map, row, col):
    if _map[row][col] == WALL:
        _wall.append(Wall(row, col, BLUE))

    # hidden else later
    else:
        pass
        # _road.append(Food(row, col, BLOCK_SIZE // 3, BLOCK_SIZE // 3, GREEN))

    if _map[row][col] == FOOD:
        _food.append(Food(row, col, BLOCK_SIZE, BLOCK_SIZE, YELLOW))
        _food_Position.append([row, col])

    if _map[row][col] == MONSTER:
        _ghost.append(Player(row, col, IMAGE_GHOST[len(_ghost) % len(IMAGE_GHOST)]))
        _ghost_Position.append([row, col])


def initData() -> None:
    global N, M, _map, _food_Position, _food, _road, _wall, _ghost, _visited, Score, _state_PacMan, _ghost_Position
    N = M = Score = _state_PacMan = 0
    _map = []
    _wall = []
    _road = []
    _food = []
    _ghost = []
    _food_Position = []
    _ghost_Position = []

    readMapInFile(map_name=Map_name)
    _visited = [[0 for _ in range(M)] for _ in range(N)]

    for row in range(N):
        for col in range(M):
            check_Object(_map, row, col)


def Draw(_screen) -> None:
    for wall in _wall:
        wall.draw(_screen)
    for road in _road:
        road.draw(_screen)
    for food in _food:
        food.draw(_screen)
    for ghost in _ghost:
        ghost.draw(_screen)

    PacMan.draw(_screen)

    text_surface = my_font.render('Score: {Score}'.format(Score=Score), False, RED)
    screen.blit(text_surface, (0, 0))


# 1: Random, 2: A*
def generate_Ghost_new_position(_ghost, _type: int = 0) -> list[list[int]]:
    _ghost_new_position = []
    if _type == 1:
        for idx in range(len(_ghost)):
            [row, col] = _ghost[idx].getRC()

            rnd = random.randint(0, 3)
            new_row, new_col = row + DDX[rnd][0], col + DDX[rnd][1]
            while not isValid2(_map, new_row, new_col, N, M):
                rnd = random.randint(0, 3)
                new_row, new_col = row + DDX[rnd][0], col + DDX[rnd][1]

            _ghost_new_position.append([new_row, new_col])

    # update latest
    elif _type == 2:
        for idx in range(len(_ghost)):
            [start_row, start_col] = _ghost[idx].getRC()
            [end_row, end_col] = PacMan.getRC()
            _ghost_new_position.append(Ghost_move_level4(_map, start_row, start_col, end_row, end_col, N, M))

    return _ghost_new_position


def check_collision_ghost(_ghost, pac_row=-1, pac_col=-1) -> bool:
    Pac_pos = [pac_row, pac_col]
    if pac_row == -1:
        Pac_pos = PacMan.getRC()
    for g in _ghost:
        Ghost_pos = g.getRC()
        if Pac_pos == Ghost_pos:
            return True

    return False


def change_direction_PacMan(new_row, new_col):
    global PacMan, _state_PacMan
    [current_row, current_col] = PacMan.getRC()
    _state_PacMan = (_state_PacMan + 1) % len(IMAGE_PACMAN)

    if new_row > current_row:
        PacMan.change_state(-90, IMAGE_PACMAN[_state_PacMan])
    elif new_row < current_row:
        PacMan.change_state(90, IMAGE_PACMAN[_state_PacMan])
    elif new_col > current_col:
        PacMan.change_state(0, IMAGE_PACMAN[_state_PacMan])
    elif new_col < current_col:
        PacMan.change_state(180, IMAGE_PACMAN[_state_PacMan])


def randomPacManNewPos(_map, row, col, _N, _M):
    for [d_r, d_c] in DDX:
        new_r, new_c = d_r + row, d_c + col
        if isValid2(_map, new_r, new_c, _N, _M):
            return [new_r, new_c]


def startGame() -> None:
    global _map, _visited, Score
    _ghost_new_position = []
    result = []
    new_PacMan_Pos: list = []
    initData()
    pac_can_move = True

    done = False
    is_moving = False
    timer = 0

    status = 0
    delay = 100

    # ----------------- Run pygame
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showMenu()
                return

        if delay > 0:
            delay -= 1
        # handle move step by step
        if delay <= 0:
            if is_moving:
                timer += 1
                # Ghost move
                if len(_ghost_new_position) > 0:
                    for idx in range(len(_ghost)):
                        [old_row_Gho, old_col_Gho] = _ghost[idx].getRC()
                        [new_row_Gho, new_col_Gho] = _ghost_new_position[idx]

                        if old_row_Gho < new_row_Gho:
                            _ghost[idx].move(1, 0)
                        elif old_row_Gho > new_row_Gho:
                            _ghost[idx].move(-1, 0)
                        elif old_col_Gho < new_col_Gho:
                            _ghost[idx].move(0, 1)
                        elif old_col_Gho > new_col_Gho:
                            _ghost[idx].move(0, -1)

                        if timer >= SIZE_WALL:
                            _ghost[idx].setRC(new_row_Gho, new_col_Gho)

                            _map[old_row_Gho][old_col_Gho] = EMPTY
                            _map[new_row_Gho][new_col_Gho] = MONSTER

                            # check touch Food
                            for index in range(len(_food)):
                                [row_food, col_food] = _food[index].getRC()
                                if row_food == old_row_Gho and col_food == old_col_Gho:
                                    _map[row_food][col_food] = FOOD

                # Pacman move
                if len(new_PacMan_Pos) > 0:
                    [old_row_Pac, old_col_Pac] = PacMan.getRC()
                    [new_row_Pac, new_col_Pac] = new_PacMan_Pos

                    if old_row_Pac < new_row_Pac:
                        PacMan.move(1, 0)
                    elif old_row_Pac > new_row_Pac:
                        PacMan.move(-1, 0)
                    elif old_col_Pac < new_col_Pac:
                        PacMan.move(0, 1)
                    elif old_col_Pac > new_col_Pac:
                        PacMan.move(0, -1)

                    if timer >= SIZE_WALL or PacMan.touch_New_RC(new_row_Pac, new_col_Pac):
                        is_moving = False
                        PacMan.setRC(new_row_Pac, new_col_Pac)
                        Score -= 1

                        # check touch Food
                        for idx in range(len(_food)):
                            [row_food, col_food] = _food[idx].getRC()
                            if row_food == new_row_Pac and col_food == new_col_Pac:
                                _map[row_food][col_food] = EMPTY
                                _food.pop(idx)
                                _food_Position.pop(idx)
                                Score += 20
                                break
                        new_PacMan_Pos = []

                if check_collision_ghost(_ghost):
                    pac_can_move = False
                    done = True
                    status = -1

                if len(_food_Position) == 0:
                    status = 1
                    done = True

                if timer >= SIZE_WALL:
                    is_moving = False
            else:
                # _type = [0:don't move(default), 1:Random, 2:A*]
                if Level == 3:
                    _ghost_new_position = generate_Ghost_new_position(_ghost, _type=1)
                elif Level == 4:
                    _ghost_new_position = generate_Ghost_new_position(_ghost, _type=2)
                else:
                    _ghost_new_position = generate_Ghost_new_position(_ghost, _type=0)

                is_moving = True
                timer = 0

                if not pac_can_move:
                    continue

                [row, col] = PacMan.getRC()

                # cài đặt thuật toán ở đây, thay đổi ALGORITHM trong file constants.py
                # thuật toán chỉ cần trả về vị trí mới theo format [new_row, new_col] cho biến new_PacMan_Pos
                # VD: new_PacMan_Pos = [4, 5]
                # thuật toán sẽ được cài đặt trong folder Algorithms

                search = SearchAgent(_map, _food_Position, row, col, N, M)
                if Level == 1 or Level == 2:
                    if len(result) <= 0:
                        result = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL1"])
                        if len(result) > 0:
                            result.pop(0)
                            new_PacMan_Pos = result[0]

                    elif len(result) > 1:
                        result.pop(0)
                        new_PacMan_Pos = result[0]

                elif Level == 3 and len(_food_Position) > 0:
                    new_PacMan_Pos = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL3"], visited=_visited)
                    _visited[row][col] += 1

                elif Level == 4 and len(_food_Position) > 0:
                    new_PacMan_Pos = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL4"], depth=4, Score=Score)

                if len(_food_Position) > 0 and (len(new_PacMan_Pos) == 0 or [row, col] == new_PacMan_Pos):
                    new_PacMan_Pos = randomPacManNewPos(_map, row, col, N, M)
                if len(new_PacMan_Pos) > 0:
                    change_direction_PacMan(new_PacMan_Pos[0], new_PacMan_Pos[1])
                    if check_collision_ghost(_ghost, new_PacMan_Pos[0], new_PacMan_Pos[1]):
                        pac_can_move = False
                        done = True
                        status = -1

        # ------------------------------------------------------

        screen.fill(BLACK)
        Draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    handleEndGame(status)


done_2 = False


def handleEndGame(status: int):
    global done_2
    done_2 = False
    bg = pygame.image.load("images/gameover_bg.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    bg_w = pygame.image.load("images/win.jpg")
    bg_w = pygame.transform.scale(bg_w, (WIDTH, HEIGHT))

    def clickContinue():
        global done_2
        done_2 = True

    def clickQuit():
        pygame.quit()
        sys.exit(0)

    btnContinue = Button(WIDTH // 2 - 300, HEIGHT // 2 - 50, 200, 100, screen, "CONTINUE", clickContinue)
    btnQuit = Button(WIDTH // 2 + 50, HEIGHT // 2 - 50, 200, 100, screen, "QUIT", clickQuit)

    delay = 100
    while not done_2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        if delay > 0:
            delay -= 1
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if status == -1:
            screen.blit(bg, (0, 0))
        else:
            screen.blit(bg_w, (0, 0))
            text_surface = my_font_2.render('Your Score: {Score}'.format(Score=Score), False, RED)
            screen.blit(text_surface, (WIDTH // 4 - 65, 10))

        btnQuit.process()
        btnContinue.process()

        pygame.display.flip()
        clock.tick(FPS)

    showMenu()


def showMenu():
    _menu = Menu(screen)
    global Level, Map_name
    [Level, Map_name] = _menu.run()
    startGame()


if __name__ == '__main__':
    showMenu()
    pygame.quit()
