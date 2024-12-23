from typing import List

class Solution:
    def _combinationSum(self, candidates: List[int], i: int, target: int) -> List[List[int]]:
        if i >= len(candidates):
            return []
        if candidates[i] > target:
            return []
        if candidates[i] == target:
            return [[target]]
        if (i, target) in self.record:
            return self.record[(i, target)]
        ret = []
        n = i
        while candidates[n] == candidates[i]:
            n += 1
        ret0 = self._combinationSum(candidates, i+1, target - candidates[i])
        ret.extend([candidates[i]] + e for e in ret0 if len(e) > 0)
        ret1 = self._combinationSum(candidates, n, target)
        ret.extend([list(e) for e in ret1 if len(e) > 0])
        self.record[(i, target)] = ret
        return ret

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        self.record = {}
        return self._combinationSum(candidates, 0, target)

arr = [2, 5, 2, 1, 2]
target = 5

s = Solution()
ret = s.combinationSum2(arr, target)
print(ret)
