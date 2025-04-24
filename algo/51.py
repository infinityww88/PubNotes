class Solution:
    def empty(self, matrix, i, j, n):
        return i < 0 or i >= n or j < 0 or j >= n or matrix[i][j] == False
    def isOk(self, matrix, i, j, n):
        if not all(self.empty(matrix, i, k, n) for k in range(n)):
            return False
        if not all(self.empty(matrix, k, j, n) for k in range(n)):
            return False
        x, y = 0, j - i
        if not all(self.empty(matrix, x + k, y + k, n) for k in range(n)):
            return False
        x, y = 0, j + i
        if not all(self.empty(matrix, x + k, y - k, n) for k in range(n)):
            return False
        return True
    def dfs(self, matrix, i, n):
        if i == n:
            self.ret.append([''.join('Q' if e else '.' for e in row) for row in matrix])
            return
        for j in range(n):
            if self.isOk(matrix, i, j, n):
                matrix[i][j] = True
                self.dfs(matrix, i + 1, n)
                matrix[i][j] = False
    def solveNQueens(self, n: int) -> list[list[str]]:
        matrix = [[False] * n for i in range(n)]
        self.ret = []
        self.dfs(matrix, 0, n)
        return self.ret

s = Solution()
ret = s.solveNQueens(8)
print(ret)