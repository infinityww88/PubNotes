from typing import List

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stk = []
        for token in tokens:
            if token == '+':
                a = stk.pop()
                b = stk.pop()
                stk.append(b+a)
            elif token == '-':
                a = stk.pop()
                b = stk.pop()
                stk.append(b-a)
            elif token == '*':
                a = stk.pop()
                b = stk.pop()
                stk.append(b*a)
            elif token == '/':
                a = stk.pop()
                b = stk.pop()
                stk.append(int(b/a))
            else:
                stk.append(int(token))
        return stk[0]

s = Solution()
test = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
ret = s.evalRPN(test)
print(ret)