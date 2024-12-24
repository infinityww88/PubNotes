from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        maxSum = nums[0]
        lastSum = nums[0]
        for i in range(1, len(nums)):
            currSum = max(lastSum + nums[i], nums[i])
            maxSum = max(currSum, maxSum)
            lastSum = currSum
        return maxSum

nums = [5,4,-1,7,8]
print(Solution().maxSubArray(nums))