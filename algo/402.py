class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        ret = []
        n = len(num) - k
        for c in num:
            while k > 0 and ret and ret[-1] > c:
                ret.pop()
                k -= 1
            ret.append(c)
        ret = ret[:n]
        i = 0
        while i < len(ret) and ret[i] == '0':
            i += 1
        ret = ret[i:]
        return ''.join(ret) if ret else '0'

s = Solution()
ret = s.removeKdigits("10", 2)
print(ret)
