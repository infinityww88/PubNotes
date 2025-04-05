import math

class Solution:
    def jump(self, nums) -> int:
        n = len(nums)
        steps = [10000] * n
        steps[0] = 0
        for i in range(n-1):
            for j in range(1, nums[i]+1):
                if i + j < n:
                    steps[i+j] = min(steps[i+j], steps[i] + 1)
        return steps[-1]

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
    def jump1(self, nums):
        self.record = [-1] * len(nums)
        self.record[-1] = 0
        self._jump(nums, 0)
        return self.record[0]

s = Solution()
nums = [2,3,0,1,4]
print(s.jump(nums))
