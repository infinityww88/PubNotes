class Solution:
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
print(s.removeDuplicateLetters(""))