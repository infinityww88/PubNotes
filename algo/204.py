import math

class Solution:
    def countPrimes(self, n):
        arr = [True] * (n)
        count = 0
        for i in range(2, n):
            if arr[i]:
                count += 1
                j = 2
                while i * j < n:
                    arr[i*j] = False
                    j += 1
        return count

'''
class Solution:
    def countPrimes(self, n):
        if n == 0: return 0
        if n == 1: return 0
        if n == 2: return 0
        d = [2]
        for i in range(3, n):
            t = int(math.sqrt(i))
            j = 0
            f = True
            while j < len(d) and d[j] <= t:
                if i % d[j] == 0:
                    f = False
                    break
                j += 1
            if f: d.append(i)
        return len(d)
'''

s = Solution()
t = 20
ret = s.countPrimes(t)
print(ret)