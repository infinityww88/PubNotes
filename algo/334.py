import math

class Solution:
    def increasingTriplet(self, nums):
        m1, m2 = math.inf, math.inf
        '''
        m1 m2 从第一对 a < b 开始记录，随后向两条腿走路一样交换，任何时刻总有 m2 > m1。
        m1 序列越来越小，m2 序列越来越小
        当遇到一个新的元素比 m1 m2 都大的时候就找到了三元递增序列
        注意有时 m1 会交换到 m2 的后面，由之前的 m1 m2 变成新的 m2 m1。但是这个过程中 m2 总是大于前后两个 m1 的
        这是关键。因此即使 m1 交换到 m2 后面，只要遇到新元素大于 m2，那它也必定大于 m1 的前一个 m1
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