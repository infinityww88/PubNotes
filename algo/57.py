from typing import List

class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        n, n0, n1 = len(intervals), 0, 0
        for i, v in enumerate(intervals):
            if v[1] < newInterval[0]:
                n0 = i + 1
            elif v[0] > newInterval[1]:
                n1 = n - i
                break
        ret = []
        for i in range(n0):
            ret.append(intervals[i])

        for i in range(n0, n - n1):
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
        ret.append(newInterval)

        for i in range(n1):
            ret.append(intervals[n-n1+i])
        
        return ret

s = Solution()
arr = [[1,3],[6,9]]
nl = [2, 5]
ret = s.insert(arr, nl)
print(ret)