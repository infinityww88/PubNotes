class Solution:
    def _numDistinct(self, s, t, i, j):
        if j >= len(t):
            return 1
        if len(s) - i < len(t) - j:
            return 0
        if (i, j) in self.record:
            return self.record[(i, j)]
        n = 0
        if s[i] == t[j]:
            n += self._numDistinct(s, t, i + 1, j + 1)
        n += self._numDistinct(s, t, i + 1, j)
        self.record[(i, j)] = n
        return n
    def numDistinct(self, s: str, t: str) -> int:
        self.record = {}
        return self._numDistinct(s, t, 0, 0)

s = Solution()
a = "babgbag"
b = "bag"
ret = s.numDistinct(a, b)
print(ret)