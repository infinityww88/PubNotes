from typing import List

class Solution:
    def dfs(self, k, n, start):
        if k == 0 and n == 0:
            return [[]]
        if start > 9 or start > n:
            return []
        if (k, n, start) in self.record:
            return self.record[(k, n, start)]
        ret = []
        t = self.dfs(k-1, n - start, start + 1)
        for i in t:
            ret.append([start] + i)
        t = self.dfs(k, n, start + 1)
        for i in t:
            ret.append(list(i))
        self.record[(k, n, start)] = ret
        return ret
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        self.record = {}
        ret = self.dfs(k, n, 1)
        return ret

s = Solution()
ret = s.combinationSum3(2, 18)
print(ret)