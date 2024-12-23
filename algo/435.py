class Solution:
    def eraseOverlapIntervals(self, intervals):
        intervals = sorted(intervals, key=lambda iterval: iterval[1])
        left = intervals[-1][0]
        count = 0
        for i in range(len(intervals)-2, -1, -1):
            if intervals[i][1] <= left:
                left = intervals[i][0]
            else:
                if intervals[i][0] >= left:
                    left = intervals[i][0]
                count += 1
        return count

s = Solution()
ret = s.eraseOverlapIntervals([[0,3], [1,6], [2,5],[4,7],[8,10],[9,11],[12,15],[13,14]])
print(ret)
