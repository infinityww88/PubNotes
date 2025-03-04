class Solution:
    def fractionToDecimal(self, numerator: int, denominator: int) -> str:
        sign = 1
        if numerator < 0:
            sign = -1
            numerator = -numerator
        a = numerator // denominator
        b = numerator % denominator;
        ret = []
        s = {}
        while b != 0:
            b = b * 10
            if b in s:
                #repeat
                break
            else:
                ret.append(b // denominator)
                s[b] = len(ret) - 1
                b = b % denominator
        ret = list(map(str, ret))
        if b != 0:
            i = s[b]
            ret = f"{a}.{''.join(ret[:i])}({''.join(ret[i:])})"
        elif ret:
            ret = f"{a}.{''.join(ret)}"
        else:
            ret = f"{a}"
        if sign < 0:
            return "-"+ret
        return ret

s = Solution()
ret = s.fractionToDecimal(-50, 8)
print(ret)
