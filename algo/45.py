import math

class Solution:
    def _jump(self, nums, start):
        if self.record[start] >= 0:
            return self.record[start]
        minStep = math.inf
        for i in range(1, nums[start]+1):
            if start + i >= len(nums):
                break
            t = self._jump(nums, start+i) + 1
            if minStep > t:
                minStep = t
        self.record[start] = minStep
        return minStep
    def jump(self, nums):
        self.record = [-1] * len(nums)
        self.record[-1] = 0
        self._jump(nums, 0)
        return self.record[0]

s = Solution()
nums = [2, 1]
print(s.jump(nums))
