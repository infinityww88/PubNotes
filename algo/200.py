class Solution:

    def traverse(self, grid, i, j):
        if i >= len(grid) or i < 0 or j >= len(grid[0]) or j < 0:
            return
        if grid[i][j] == "1":
            grid[i][j] = "2"
            self.traverse(grid, i+1, j)
            self.traverse(grid, i-1, j)
            self.traverse(grid, i, j+1)
            self.traverse(grid, i, j-1)
                    
    def numIslands(self, grid):
        count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "1":
                    count += 1
                    self.traverse(grid, i, j)
        return count

grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]

s = Solution()
print(s.numIslands(grid))