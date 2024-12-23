class Solution:
    def findKthLargest(self, nums, k):
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
arr = [3,2,3,1,2,4,5,5,6]
k = 4
ret = s.findKthLargest(arr, k)
print(ret)