from typing import List

class Solution:
    def separate(self, s, i, n):
        if len(s) - i < n:
            return []
        if n == 1:
            if len(s) - i > 1 and s[i] == '0':
                return []
            print(s, i, n, s[i:])
            if int(s[i:]) > 255:
                return []
            return [s[i:]]
        if (i, n) in self.record:
            return self.record[(i, n)]
        ret = []
        if s[i] == '0':
            k = self.separate(s, i+1, n-1)
            ret.extend(s[i] + '.' + e for e in k)
        else:
            for j in range(i+1, len(s)):
                if int(s[i:j]) <= 255:
                    k = self.separate(s, j, n-1)
                    ret.extend(s[i:j] + '.' + e for e in k)
        self.record[(i, n)] = ret
        return ret

    def restoreIpAddresses(self, s: str) -> List[str]:
        self.record = {}
        return self.separate(s, 0, 4)

s = Solution()
ret = s.restoreIpAddresses("0690")
print(ret)


