from typing import List

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        sn = len(s)
        wc = len(words)
        wn = len(words[0])
        ret = []
        for i in range(wn):
            remain = {}
            for w in words:
                if w not in remain:
                    remain[w] = 0
                remain[w] += 1
            l, r = i, i
            while r + wn <= sn:
                nw = s[r:r+wn]
                if nw in remain:
                    remain[nw] -= 1
                    if remain[nw] == 0:
                        del remain[nw]
                        if len(remain) == 0:
                            ret.append(l)
                    r += wn
                else:
                    while l < r:
                        t = s[l:l+wn]
                        if t not in remain:
                            remain[t] = 0
                        remain[t] += 1
                        l += wn
                        if t == s[r:r+wn]:
                            break
                    if s[r:r+wn] not in remain:
                        l, r = r+wn, r+wn
        return ret

s = Solution()

a = "lingmindraboofooowingdingbarrwingmonkeypoundcake"
words = ["fooo","barr","wing","ding","wing"]

print(s.findSubstring(a, words))
