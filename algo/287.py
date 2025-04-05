'''
这个二分查找不是在数组中进行二分，而是在正整数 1-n 之间进行二分。因为所有数字都在 1-n 之间。
left 和 right 也不是数组索引，就是简单的正整数。
每次二分，统计所有小于等于 mid 的数组元素个数，如果大于 mid，根据鸽巢原理，重复的数字一定小于等于 mid，因此让 right = mid，缩小一半的范围，否则重复数字一定大于 mid，让 left = mid + 1。
注意重复数字总是在 left-right 之间。因此当 left=right 时，就找到了重复的数字
'''
class Solution:
    def findDuplicate(self, nums: list[int]) -> int:
        slow, fast = 0, 0
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        slow = 0
        while slow != fast:
            slow= nums[slow]
            fast= nums[fast]
        return slow

    def findDuplicate1(self, nums: list[int]) -> int:
        n = len(nums)
        left, right = 1, n - 1
        while left < right:
            mid = (left + right) // 2
            count = 0
            for num in nums:
                if num <= mid:
                    count += 1
            if count > mid:
                right = mid
            else:
                left = mid + 1
        return left

s = Solution()
arr = [1, 6, 3, 4, 5, 2, 2, 7]
ret = s.findDuplicate(arr)
print(ret)