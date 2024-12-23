'''
从后向前找到第一个非递增的分界点
在后面的递增序列中中到仅比分界点大的元素，二者交换，后面序列仍然保持递增
将后面的序列反序排列
'''
class Solution:
    def nextPermutation(self, nums):
        i = len(nums) - 1
        while i > 0 and nums[i-1] >= nums[i]:
            i -= 1
        if i > 0:
            j = len(nums) - 1
            while nums[j] <= nums[i-1]:
                j -= 1
            nums[i-1], nums[j] = nums[j], nums[i-1]
        s, t = i, len(nums)-1
        while s < t:
            nums[s], nums[t] = nums[t], nums[s]
            s += 1
            t -= 1

s = Solution()
nums = [1, 1, 5]
s.nextPermutation(nums)
print(nums)