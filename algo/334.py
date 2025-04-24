import math

class Solution:
    def increasingTriplet(self, nums):
        m1, m2 = math.inf, math.inf
        '''
        m1 和 m2 总是越来越小，类似求 min 但是是求两个 min。因此 m1 和 m2 总是记录当前找到的最小的两个数，并且 m1 < m2
        当出现一个数字同时大于 m1 和 m2 时，即得到结果.
        '''
        for i in nums:
            if i <= m1:
                m1 = i
            elif i <= m2:
                m2 = i
            else:
                return True
        return False

s = Solution()
print(s.increasingTriplet([2, 1, 5, 0, 4, 6]))