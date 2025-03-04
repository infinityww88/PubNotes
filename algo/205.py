class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        d = [None] * 128
        k = [None] * 128
        if len(s) != len(t):
            return False
        n = len(s)
        for i in range(n):
            sk = ord(s[i])
            tk = ord(t[i])
            if d[sk] == None:
                if k[tk] != None:
                    return False
                d[sk] = tk
                k[tk] = True
            else:
                if d[sk] != tk:
                    return False
        return True

s = Solution()
a = "foo"
b = "bar"
ret = s.isIsomorphic(a, b)
print(ret)
