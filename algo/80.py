from typing import List

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        i = 0
        j = 1
        c = 1
        while j < len(nums):
            if nums[j] == nums[i]:
                if c == 1:
                    i += 1
                    nums[j], nums[i] = nums[i], nums[j]
                    j += 1
                    c += 1
                else:
                    j += 1
            else:
                i += 1
                nums[j], nums[i] = nums[i], nums[j]
                j += 1
                c = 1
        return i + 1

s = Solution()
ret = s.removeDuplicates([0,0,1,1,1,1,2,3,3])
print(ret)