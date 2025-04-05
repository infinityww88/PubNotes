'''
左边数字的权重最大。对于从左到右的每一位数字，如果还有可移除的机会，如果右边有比它还小的数字，就应该将它移除。
这就是单调栈。
对从左到右的每一位数字，弹出栈顶所有比它大的数字（如果还有可以出的次数），因为它更小，直到遇到比它更小的或栈为空（它最小），
让后将它加入栈中。
单调栈的入栈过程：考察栈顶元素和即将要入栈的元素，如果不符合单调性，就依次将栈顶元素弹出，直到遇到满足单调性的元素，或者栈为空，
然后将此元素加入栈中
'''
class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        stk = []
        n = len(num) - k
        for c in num:
            while k > 0 and stk and stk[-1] > c:
                stk.pop()
                k -= 1
            stk.append(c)
        '''
        上面的 while 只保证最多移除 k 个，但是不保证严格移除 k 个。例如如果 num 所有数字都是单调递增的。
        此时，while 循环体从不执行，stk 会完整 append 整个 num。因此最后要截断 stk 为 len(num) - k 个数字。
        或者在 for 循环中控制 stk 最多 append len(num) - k 个元素。
        '''
        stk = stk[:n]
        i = 0
        while i < len(stk) and stk[i] == '0':
            i += 1
        stk = stk[i:]
        return ''.join(stk) if stk else '0'

s = Solution()
ret= s.removeKdigits("10", 2)
print(ret)
