from typing import List

class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        row, col = len(matrix), len(matrix[0])
        dp = [0] * col
        maxLen = 0
        for i in range(row):
            topLeft, left = 0, 0
            for j in range(col):
                top = dp[j]
                if matrix[i][j] == '1':
                    dp[j] = min(topLeft, left, top) + 1
                else:
                    dp[j] = 0
                topLeft = top
                left = dp[j]
                maxLen = max(maxLen, dp[j])
        return maxLen * maxLen
                


s = Solution()
#ret = s.maximalSquare([["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]])
ret = s.maximalSquare([["0","1"],["1","0"]])
print(ret)
