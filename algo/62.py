class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid):
        rows = len(obstacleGrid)
        cols = len(obstacleGrid[0])
        ret = [0] * cols
        ret[0] = 1
        for i in range(rows):
            t = 0
            for j in range(cols):
                if obstacleGrid[i][j] == 1:
                    ret[j] = 0
                else:
                    ret[j] = ret[j] + t
                t = ret[j]
        return ret[-1]

s = Solution()
t = s.uniquePathsWithObstacles([[0, 1], [0, 0]])
print(t)


