class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        stk: list[int] = []
        ret = [0] * len(temperatures)
        for i in range(len(temperatures)):
            while stk and temperatures[stk[-1]] < temperatures[i]:
                ret[stk[-1]] = i - stk[-1]
                stk.pop()
            stk.append(i)
        return ret

s = Solution()
ret = s.dailyTemperatures([30, 40, 50, 60])
print(ret)