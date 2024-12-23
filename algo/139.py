from typing import List

class Solution:
    def dfs(self, s, index):
        if index >= len(s):
            return True
        if self.record[index] != -1:
            return self.record[index] == 1
        for i in range(index, len(s)):
            if s[index:i+1] in self.wordSet:
                if self.dfs(s, i+1) == 1:
                    self.record[index] = 1
                    return True
        print(s, index, self.record[index])
        self.record[index] = 0
        return False
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        self.wordSet = set()
        for w in wordDict:
            self.wordSet.add(w)
        self.record = [-1] * len(s)
        return self.dfs(s, 0)

s = Solution()
w = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab"
wd = ["a","aa","aaa","aaaa","aaaaa","aaaaaa","aaaaaaa","aaaaaaaa","aaaaaaaaa","aaaaaaaaaa"]
print(s.wordBreak(w, wd))