from typing import List

class Solution:
    def trap(self, height: list[int]) -> int:
        ret = 0
        stk = []
        for i in range(len(height)):
            lastH = 0
            while stk:
                end = stk[-1]
                w = i - end - 1
                h = min(height[end], height[i])
                area = w * (h - lastH)
                lastH = h
                ret += area
                if height[end] > height[i]:
                    break
                stk.pop()
            stk.append(i)
        return ret














class Solution1:
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

height = [0,1,0,2,1,0,1,3,2,1,2,1]
s = Solution()
ret = s.trap(height)
print(ret)
