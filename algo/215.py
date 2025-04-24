class Solution:
    def findKthLargest(self, nums, k):
        while len(nums) > 1: 
            p = nums[0]
            i, j = 1, len(nums) - 1
            while i <= j:
                if p > nums[i] and p < nums[j]:
                    #只有严格不等于 p 的元素才交换，之所以这样事因为有一种 case，中间存在大量相等的元素
                    #如果严格限定左边的区间大于等于 p，右边的元素小于 p，就会导致这些相同的大量元素总是划分到同一个区间
                    #导致每次划分不能很好地缩小问题规模
                    #只有这样处理，才可以让相同元素平均分配到两个区间，使得问题规模被很好的二分，每次问题规模尽可能地小
                    nums[i], nums[j] = nums[j], nums[i]
                    j -= 1
                    i += 1
                if p <= nums[i]:
                    i += 1
                if p >= nums[j]:
                    j -= 1
            if i == k:
                return p
            if i < k:
                nums = nums[i:]
                k = k - i
            else:
                nums = nums[1:i]
        return nums[0]

    def findKthLargest1(self, nums, k):
        n = len(nums)
        l = 0
        r = n
        while l < r:
            i, j = l + 1, r - 1
            p = nums[l]
            while i <= j:
                if nums[i] < p and nums[j] > p:
                    nums[i], nums[j] = nums[j], nums[i]
                    i += 1
                    j -= 1
                if nums[i] >= p:
                    i += 1
                if nums[j] <= p:
                    j -= 1
            c0 = i - l 
            if k == c0:
                return p
            elif k < c0:
                l += 1
                r = i
            else:
                l = i
                k -= c0

s = Solution()
arr = [3,2,1,5,6,4]
k = 2
ret = s.findKthLargest(arr, k)
print(ret)