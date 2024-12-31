class Solution:
    def reverse(self, s, i, j):
        while i < j:
            s[i], s[j] = s[j], s[i]
            i += 1
            j -= 1
    def reverseWords(self, s) -> str:
        s = list(s)
        i, j = 0, len(s)-1
        self.reverse(s, i, j)
        i, j = 0, 0
        while j < len(s):
            while i < len(s) and s[i] == ' ':
                i += 1
            j = i
            while j < len(s) and s[j] != ' ':
                j += 1
            self.reverse(s, i, j-1)
            i = j
        space = False
        i, j = 0, 0
        while j < len(s):
            if s[j] == ' ':
                if space:
                    s[i] = s[j]
                    i += 1
                    space = False
            else:
                s[i] = s[j]
                space = True
                i += 1
            j += 1
        if i-1 > 0 and s[i-1] == ' ':
            i -= 1
        return ''.join(s[:i])

s = Solution()
ret = s.reverseWords("abc")
print(ret+"|")
        

