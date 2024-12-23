from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        s2e = dict()
        e2s = dict()

        lcs = 0
        for i in nums:
            if i in s2e or i in e2s:
                continue
            s, e = i, i
            if i - 1 in e2s:
                s0, e0 = e2s[i-1], i-1
                del s2e[s0]
                del e2s[e0]
                s = s0
            if i + 1 in s2e:
                s0, e0 = i+1, s2e[i+1]
                del s2e[s0]
                del e2s[e0]
                e = e0
            s2e[s] = e
            e2s[e] = s
            if lcs < e - s + 1:
                lcs = e - s + 1
        return lcs

s = Solution()
ret = s.longestConsecutive([0,3,7,2,5,8,4,6,0,1])
print(ret)