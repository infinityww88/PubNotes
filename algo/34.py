class Solution:
    def searchRange(self, nums, target: int):
        p0, p1 = -1, -1
        l, r = 0, len(nums)-1
        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                if m == 0 or nums[m-1] < nums[m]:
                    p0 = m
                    break
                else:
                    r = m - 1
            elif nums[m] > target:
                r = m - 1
            else:
                l = m + 1

        l, r = 0, len(nums)-1
        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                if m == len(nums)-1 or nums[m] < nums[m+1]:
                    p1 = m
                    break
                else:
                    l = m + 1
            elif nums[m] < target:
                l = m + 1
            else:
                r = m - 1
        return [p0, p1]
        
s = Solution()
ret = s.searchRange([1, 4], 4)
print(ret)
