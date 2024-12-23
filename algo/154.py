from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        while l < r:
            i = nums[r]
            if r > l and nums[r] == nums[l]:
                r -= 1
            else:
                m = (l + r) // 2
                if nums[m-1] > nums[m]:
                    return nums[m]
                if nums[m] >= nums[l] and nums[l] > nums[r]:
                    l = m + 1
                else:
                    r = m - 1
        return nums[l]

s = Solution()
ret = s.findMin([3, 1])
print(ret)