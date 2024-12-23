class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        record = set()
        l, r = 0, 0
        maxLen = 0
        while r < len(s):
            c = s[r]
            if c not in record:
                r += 1
                record.add(c)
                maxLen = max(r - l, maxLen)
            else:
                record.remove(s[l])
                l += 1
        return maxLen

s = Solution()
print(s.lengthOfLongestSubstring(""))
