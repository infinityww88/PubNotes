from typing import List

class Solution:
    def collect(self, board, i, j, cells):
        if i < 0 or i >= self.rows or j < 0 or j >= self.cols:
            return
        if board[i][j] != 'O':
            return
        cells.append((i, j))
        board[i][j] = 'X'
        self.collect(board, i-1, j, cells)
        self.collect(board, i+1, j, cells)
        self.collect(board, i, j-1, cells)
        self.collect(board, i, j+1, cells)
        
    def solve(self, board: List[List[str]]) -> None:
        self.rows = len(board)
        self.cols = len(board[0])
        cells = []
        for i in range(self.rows):
            for j in range(self.cols):
                cells.clear()
                self.collect(board, i, j, cells)
                surrounded = 'Y'
                for x, y in cells:
                    if x == 0 or x == (self.rows-1) or y == 0 or y == (self.cols-1):
                        surrounded = 'N'
                for x, y in cells:
                    board[x][y] = surrounded
        for i in range(self.rows):
            for j in range(self.cols):
                if board[i][j] == 'Y':
                    board[i][j] = 'X'
                if board[i][j] == 'N':
                    board[i][j] = 'O'

s = Solution()
board = [
    ["O","X","O","O","O","O","O","O","O"],
    ["O","O","O","X","O","O","O","O","X"],
    ["O","X","O","X","O","O","O","O","X"],
    ["O","O","O","O","X","O","O","O","O"],
    ["X","O","O","O","O","O","O","O","X"],
    ["X","X","O","O","X","O","X","O","X"],
    ["O","O","O","X","O","O","O","O","O"],
    ["O","O","O","X","O","O","O","O","O"],
    ["O","O","O","O","O","X","X","O","O"]]
s.solve(board)
print(board)