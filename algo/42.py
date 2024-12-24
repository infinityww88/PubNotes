from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        stk = []
        stk.append(0)
        ret = 0
        for i in range(1, len(height)):
            h = height[i]
            lastH = 0
            while stk:
                idx = stk[-1]
                w = i - idx - 1
                newH = min(height[idx], h)
                ret += w * (newH - lastH)
                lastH = height[idx]
                if height[idx] > h:
                    break
                stk.pop()
            stk.append(i)
        return ret

height = [1, 2, 2]
s = Solution()
ret = s.trap(height)
print(ret)
