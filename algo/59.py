from typing import List

class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        mat = [[0] * n for i in range(n)]
        l, r, t, b = 0, n-1, 0, n-1
        base = 1
        while l <= r:
            if l == r:
                mat[t][l] = base
                break
            k = r - l
            for i in range(0, k):
                mat[t][l+i] = base + i
                mat[t+i][r] = base + i + k
                mat[b][r-i] = base + i + k + k
                mat[b-i][l] = base + i + k + k + k
            base += k * 4
            l += 1
            r -= 1
            t += 1
            b -= 1
        return mat

s = Solution()
ret = s.generateMatrix(4)
print(ret)