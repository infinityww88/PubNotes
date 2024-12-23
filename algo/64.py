from typing import List

class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        row = len(grid)
        col = len(grid[0])
        arr = [100000000] * col
        arr[0] = grid[0][0]
        for i in range(1, col):
            arr[i] = arr[i-1] + grid[0][i]
        for i in range(1, row):
            for j in range(col):
                if j == 0:
                    arr[0] = grid[i][0] + arr[0]
                else:
                    arr[j] = min(arr[j], arr[j-1]) + grid[i][j]
        return arr[-1]

s = Solution()
print(s.minPathSum([[1,3,1],[1,5,1],[4,2,1]]))
