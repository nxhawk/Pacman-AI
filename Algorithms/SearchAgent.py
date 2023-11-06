from Algorithms.AStar import AStar
from Algorithms.AlphaBetaPruning import AlphaBetaAgent
from Algorithms.BFS import BFS
from Algorithms.DFS import DFS
from Algorithms.Expectimax import ExpectAgent
from Algorithms.LocalSearch import local_search
from Algorithms.Minimax import minimaxAgent


class SearchAgent:
    def __init__(self, _map, _food_Position, start_row, start_col, N, M):
        self.map = _map.copy()
        self.food_Position = _food_Position.copy()
        self.start_row = start_row
        self.start_col = start_col
        self.N = N
        self.M = M

    def execute(self, ALGORITHMS, visited=None, depth=4, Score=0):
        if ALGORITHMS == "BFS":
            return BFS(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "DFS":
            return DFS(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "A*":
            return AStar(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "Local Search":
            return local_search(self.map, self.start_row, self.start_col, self.N, self.M, visited.copy())
        if ALGORITHMS == "Minimax":
            return minimaxAgent(self.map, self.start_row, self.start_col, self.N, self.M, depth, Score)
        if ALGORITHMS == "AlphaBetaPruning":
            return AlphaBetaAgent(self.map, self.start_row, self.start_col, self.N, self.M, depth, Score)
        if ALGORITHMS == "Expect":
            return ExpectAgent(self.map, self.start_row, self.start_col, self.N, self.M, depth, Score)
