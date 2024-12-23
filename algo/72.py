class Solution:
    def dfs(self, word1, i1, len1, word2, i2, len2, record):
        if i1 == len1: return len2 - i2
        if i2 == len2: return len1 - i1
        if record[i1][i2] != None:
            return record[i1][i2]
        distance = None
        if word1[i1] == word2[i2]:
            distance = self.dfs(word1, i1+1, len1, word2, i2+1, len2, record)
        else:
            d0 = self.dfs(word1, i1+1, len1, word2, i2, len2, record)
            d1 = self.dfs(word1, i1, len1, word2, i2 + 1, len2, record)
            d2 = self.dfs(word1, i1+1, len1, word2, i2 + 1, len2, record)
            distance = min(d0, d1, d2) + 1
        record[i1][i2] = distance
        return distance
    def minDistance(self, word1: str, word2: str) -> int:
        len1 = len(word1)
        len2 = len(word2)
        record = [[None] * len2 for i in range(len1)]
        return self.dfs(word1, 0, len1, word2, 0, len2, record)

s = Solution()
ret = s.minDistance("intention", "execution")
print(ret)