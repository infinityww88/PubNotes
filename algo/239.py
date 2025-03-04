from typing import List
from collections import deque

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        dq = deque()
        ret: List[int] = []
        for i in range(len(nums)):
            if dq and dq[0] < i - k + 1:
                dq.popleft()
            while dq and nums[dq[-1]] < nums[i]:
                dq.pop()
            dq.append(i)
            if i - k + 1 >= 0:
                ret.append(nums[dq[0]])
        return ret

class Solution1:
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
nums = [1,3,-1,-3,5,3,6,7]
k = 3
ret = s.maxSlidingWindow(nums, k)
print(ret)
