from typing import List

'''
使用单步调试的方法来理解算法的原理

一个 height 可能构成的最大矩形有它最左边开始小于它的边界，和右边开始小于它的边界确定
单调栈可以记录每个元素最左边开始小于它的边界。单调栈是递增的。每当右边元素开始小于栈顶，说明遇到了右边界。
此时开始以此弹出栈元素。每个栈元素到达下一个栈元素之间的数组元素都是大于这个栈顶元素的，这是始终维持单调栈性质保证的。从弹出的元素到当前遇到的有边界开始计算矩形面积，同时统计最大矩形面积。
当栈顶元素开始小于当前右边界，说明栈顶元素构成的矩形当前还不是最大的，还要向右延伸。将当前元素压入栈中，维持单调栈性质。
在数组两边各插入一个 0，并不影响问题的解，但是可以简化程序的判断。左边的 0 使每个数组元素以相同的方式被处理，右边的 0 保证数组中所有元素都被弹出，最后只剩下两个 0.
'''

class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        heights.insert(0, 0)
        heights.append(0)
        maxRect = 0
        stk = [0]
        for i in range(1, len(heights)):
            h = heights[i]
            while h < heights[stk[-1]]:
                t = heights[stk[-1]]
                stk.pop()
                rect = (i - stk[-1] - 1) * t
                maxRect = max(maxRect, rect)
            stk.append(i)
        return maxRect
        
s = Solution()
heights = [2,1,5,6,2,3]
ret = s.largestRectangleArea(heights)
print(ret)


# 单调栈精简
'''
class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        heights.insert(0, 0)
        heights.append(0)
        stack = [0]
        result = 0
        for i in range(1, len(heights)):
            while stack and heights[i] < heights[stack[-1]]:
                mid_height = heights[stack[-1]]
                stack.pop()
                if stack:
                    # area = width * height
                    area = (i - stack[-1] - 1) * mid_height
                    result = max(area, result)
            stack.append(i)
        return result
'''



