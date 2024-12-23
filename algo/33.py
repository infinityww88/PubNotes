class Solution:
    def search(self, nums, target: int):
        n = len(nums)
        l, r = 0, n - 1
        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                return m
            if nums[m] >= nums[l]:
                if nums[m] > target and target >= nums[l]:
                    r = m - 1
                else:
                    l = m + 1
            else:
                if nums[m] < target and target <= nums[r]:
                    l = m + 1
                else:
                    r = m - 1
        return -1

s = Solution()
print(s.search([4,5,6,7,0,1,2], 0))