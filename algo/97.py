class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        self.record = {}
        ret = self._isInterleave(s1, s2, s3)
        return ret

    def _isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        if s2 == "":
            return s1 == s3
        if s1 == "":
            return s2 == s3
        if (s1, s2, s3) in self.record:
            return self.record[(s1, s2, s3)]
        i, j = 0, 0
        while i < len(s1) and j < len(s3) and s1[i] == s3[j]:
            i += 1
            j += 1
            if self._isInterleave(s2, s1[i:], s3[j:]):
                self.record[(s1, s2, s3)] = True
                return True
        s1, s2 = s2, s1
        i, j = 0, 0
        while i < len(s1) and j < len(s3) and s1[i] == s3[j]:
            i += 1
            j += 1
            if self._isInterleave(s2, s1[i:], s3[j:]):
                self.record[(s1, s2, s3)] = True
                return True
        s1, s2 = s2, s1
        self.record[(s1, s2, s3)] = False
        return False

s = Solution()
#print(s.isInterleave("aabcc", "dbbca", "aadbbcbcac"))
#print(s.isInterleave("aa", "ab", "abaa"))
print(s.isInterleave("bcbccabcccbcbbbcbbacaaccccacbaccabaccbabccbabcaabbbccbbbaa",
    "ccbccaaccabacaabccaaccbabcbbaacacaccaacbacbbccccbac",
    "bccbcccabbccaccaccacbacbacbabbcbccbaaccbbaacbcbaacbacbaccaaccabcaccacaacbacbacccbbabcccccbababcaabcbbcccbbbaa"))
