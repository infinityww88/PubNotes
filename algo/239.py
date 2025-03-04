from typing import List
from collections import deque

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        if not nums or k == 0:
            return []
    
        dq = deque()  # 存储索引的双端队列
        result = []
        
        for i in range(len(nums)):
            # 移除不在当前窗口范围内的索引
            if dq and dq[0] < i - k + 1:
                dq.popleft()
            
            # 移除所有比当前元素小的元素，保证队列单调递减
            while dq and nums[i] >= nums[dq[-1]]:
                dq.pop()
            
            # 添加当前元素的索引
            dq.append(i)
            
            # 当滑动窗口形成后，记录最大值
            if i >= k - 1:
                result.append(nums[dq[0]])
        
        return result

s = Solution()
nums = [6, 7, 8, 9, 5, 4, 3, 2, 1]
k = 4
ret = s.maxSlidingWindow(nums, k)
print(ret)
