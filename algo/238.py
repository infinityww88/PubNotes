from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [1] * n
        t = 1
        for i in range(1, n):
            ans[i] = ans[i-1] * nums[i-1]
        ans1 = [1] * n
        for i in range(n-2, -1, -1):
            ans1[i] = ans1[i+1] * nums[i+1]
        ret = [1] * n
        for i in range(n):
            ret[i] = ans[i] * ans1[i]
        return ret

s = Solution()
ret = s.productExceptSelf([1,2,3,4])
print(ret)
