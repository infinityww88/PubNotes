from typing import List

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        i, j = 0, 0
        sum = 0
        minLen = 10000000
        while j <= len(nums):
            if sum < target:
                if j < len(nums):
                    sum += nums[j]
                    if sum >= target:
                        minLen = min(minLen, j + 1 - i)
                j += 1
            else:
                sum -= nums[i]
                if sum >= target:
                        minLen = min(minLen, j - (i + 1))
                i += 1
        return minLen if minLen != 10000000 else 0

s = Solution()
print(s.minSubArrayLen(11, [1,1,1,1,1,1,1,1]))