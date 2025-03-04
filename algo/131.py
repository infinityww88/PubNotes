from typing import List

class Solution:
    def partition(self, s: str) -> List[List[str]]:
        m = [ [ [s[0]] ] ]
        for i in range(1, len(s)):
            mi, q = [], set()
            for t in m[-1]:
                mi.append(t + [s[i]])
                for k in ["", t[-1]]:
                    if k in q:
                        continue
                    q.add(k)
                    j = i - 1 - len(k)
                    if j == 0 and s[j] == s[i]:
                        mi.append([s[:i+1]])
                    elif j > 0 and s[j] == s[i]:
                        mi.extend(p + [s[j:i+1]] for p in m[j-1])
            m.append(mi)
        return min(map(len, m[-1])) - 1

s = Solution()
test = "ababababababababababababcbabababababababababababa"
ret = s.partition(test)
print(ret)