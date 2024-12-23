from typing import List

class Solution:
    def _generateParenthesis(self, n: int) -> List[str]:
        if self.record[n] != None:
            return self.record[n]
        ret = []
        for i in range(0, n):
            s0 = self._generateParenthesis(i)
            s1 = self._generateParenthesis(n-1-i)
            ret.extend(f"({a}){b}" for a in s0 for b in s1)
        self.record[n] = ret
        return ret

    def generateParenthesis(self, n: int) -> List[str]:
        self.record = [None] * (n+1)
        self.record[0] = [""]
        self.record[1] = ["()"]
        return self._generateParenthesis(n)

s = Solution()
ret = s.generateParenthesis(1)
print(ret)