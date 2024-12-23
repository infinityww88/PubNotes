class Solution:
    letters = {
        "2": ["a", "b", "c"],
        "3": ["d", "e", "f"],
        "4": ["g", "h", "i"],
        "5": ["j", "k", "l"],
        "6": ["m", "n", "o"],
        "7": ["p", "q", "r", "s"],
        "8": ["t", "u", "v"],
        "9": ["w", "x", "y", "z"],
               }
    def letterCombinations(self, digits):
        ret = []
        if digits == "":
            return ret
        ret.extend(self.letters[digits[0]])
        for i in digits[1:]:
            t = []
            for j in self.letters[i]:
                for k in ret:
                    t.append(k + j)
            ret = t
        return ret

s = Solution()
print(s.letterCombinations("232"))