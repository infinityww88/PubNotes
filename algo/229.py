from typing import List

class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        n0, n1 = 0, 0
        c0, c1 = 0, 0
        for n in nums:
            if n == n0:
                c0 += 1
            elif n == n1:
                c1 += 1
            elif c0 == 0:
                n0 = n
                c0 = 1
            elif c1 == 0:
                n1 = n
                c1 = 1
            else:
                c0 -= 1
                c1 -= 1
        c0, c1 = 0, 0
        for n in nums:
            if n == n0:
                c0 += 1
            elif n == n1:
                c1 += 1
        ret = []
        if c0 > len(nums) / 3:
            ret.append(n0)
        if c1 > len(nums) / 3:
            ret.append(n1)
        return ret

s = Solution()
print(s.majorityElement([3, 2, 3]))