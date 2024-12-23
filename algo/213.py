from typing import List

class Solution:
    def dfs(self, nums, start):
        if start >= len(nums):
            return 0
        if self.record[start] >= 0:
            return self.record[start]
        v0 = nums[start] + self.dfs(nums, start + 2)
        v1 = self.dfs(nums, start + 1)
        v = max(v0, v1)
        self.record[start] = v
        self.maxVal = max(self.maxVal, v)
        return v
    def rob(self, nums: List[int]) -> int:
        self.record = [-1] * len(nums)
        self.maxVal = 0
        self.dfs(nums[:-1], 2)
        v0 = nums[0] + self.maxVal

        self.record = [-1] * len(nums)
        self.maxVal = 0
        self.dfs(nums[1:], 0)
        v1 = self.maxVal

        v = max(v0, v1)
        return v

s = Solution()
ret = s.rob([2, 1])
print(ret)