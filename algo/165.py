class Solution:
    def compareVersion(self, version1: str, version2: str) -> int:
        p1 = version1.split(".")
        p2 = version2.split(".")
        if len(p1) > len(p2):
            p1, p2 = p2, p1
        n = max(len(p1), len(p2))
        for i in range(n):
            print(p2[i])
            i0 = 0 if i >= len(p1) else int(p1[i])
            i1 = int(p2[i])
            if i0 < i1:
                return -1
            elif i0 > i1:
                return 1
        return 0