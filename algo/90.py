from typing import List

class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        ret = [[]]
        start = 0
        for i, n in enumerate(nums):
            c = len(ret)
            if i > 0 and n == nums[i-1]:
                for j in range(start, c):
                    ret.append(ret[j] + [n])
            else:
                for j in range(c):
                    ret.append(ret[j] + [n])
            start = c
        return ret

s = Solution()
ret = s.subsetsWithDup([1, 2, 2])
print(ret)