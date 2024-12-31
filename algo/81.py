from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> bool:
        l, r = 0, len(nums) - 1
        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                return True
            if nums[l] == nums[r]:
                r -= 1
            else:
                if nums[l] > nums[r]:
                    if nums[l] <= nums[m]:
                        if target >= nums[l] and target < nums[m]:
                            r = m - 1
                        else:
                            l = m + 1
                    else:
                        if target > nums[m] and target < nums[l]:
                            l = m + 1
                        else:
                            r = m - 1
                else:
                    if target < nums[m]:
                        r = m - 1
                    else:
                        l = m + 1
        return False

s = Solution()
test = [3, 1]
target = 1
print(s.search(test, target))
