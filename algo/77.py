from typing import List

class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        record = [[] for i in range(k+1)]
        record[0] = [[]]
        for i in range(1, n+1):
            for j in range(min(i, k), 0, -1):
                record[j].extend([i] + r for r in record[j-1])
        return record[k]

s = Solution()
ret = s.combine(4, 3)
print(ret)