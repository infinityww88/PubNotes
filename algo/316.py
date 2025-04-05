from collections import Counter
class Solution:
    def removeDuplicateLetters(self, s: str) -> str:
        counter = Counter(s)
        stk: list[str] = []
        in_stk: set[str] = set()
        for c in s:
            counter[c] -= 1
            if c in in_stk:
                continue
            while stk and stk[-1] >= c and counter[stk[-1]] > 0:
                in_stk.remove(stk[-1])
                stk.pop()
            stk.append(c)
            in_stk.add(c)
        return "".join(stk)

class Solution1:
    def removeDuplicateLetters(self, s: str) -> str:
        atoi = lambda letter : ord(letter) - ord('a')
        count = [0] * 26
        stack = []
        inStack = [False] * 26
        for i in s:
            count[atoi(i)] += 1
        for i in s:
            count[atoi(i)] -= 1
            if inStack[atoi(i)]:
                continue
            while len(stack) > 0 and atoi(stack[-1]) > atoi(i) and count[atoi(stack[-1])] > 0:
                inStack[atoi(stack[-1])] = False
                stack.pop()
            stack.append(i)
            inStack[atoi(i)] = True
        return ''.join(stack)

s = Solution()
print(s.removeDuplicateLetters("abacb"))