from typing import List

class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        while l <= r:
            if l == r:
                return l
            m = (l + r) // 2
            if m == 0:
                if nums[m] > nums[m+1]:
                    return m
                else:
                    l = m + 1
            elif nums[m-1] < nums[m] and nums[m] > nums[m+1]:
                return m
            else:
                if nums[m-1] > nums[m]:
                    r = m - 1
                else:
                    l = m + 1
        return -1

s = Solution()
test = [1,2,1,3,5,6,4]
ret = s.findPeakElement(test)
print(ret)