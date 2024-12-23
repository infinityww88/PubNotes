class Solution:
    NUM = 0
    OP = 1
    EOF = -1
    def nextToken(self, s, i):
        while i < len(s) and s[i] == " ":
            i += 1
        if i >= len(s):
            return (None, Solution.EOF, i)
        if ord(s[i]) >= ord('0') and ord(s[i]) <= ord('9'):
            sum = 0
            while i < len(s) and ord(s[i]) >= ord('0') and ord(s[i]) <= ord('9'):
                sum = sum * 10 + ord(s[i]) - ord('0')
                i += 1
            return (sum, Solution.NUM, i)
        i += 1
        return (s[i-1], Solution.OP, i)

    def calcTop(self, numStack, opStack):
        b = numStack.pop()
        a = numStack.pop()
        op = opStack.pop()
        c = 0
        if op == "+": c = a + b
        if op == "-": c = a - b
        if op == "*": c = a * b
        if op == "/": c = a // b
        numStack.append(c)
            
    def calculate(self, s: str) -> int:
        i = 0
        numStack = []
        opStack = []
        opPriority = {"+": 0, "-": 0, "*": 1, "/": 1}
        while i < len(s):
            token, type, i = self.nextToken(s, i)
            if type == Solution.EOF:
                break
            if type == Solution.NUM:
                numStack.append(token)
            else:
                if len(opStack) == 0 or opPriority[token] > opPriority[opStack[-1]]:
                    opStack.append(token)
                else:
                    while len(opStack) > 0 and opPriority[token] <= opPriority[opStack[-1]]:
                        self.calcTop(numStack, opStack)
                    opStack.append(token)
        while len(opStack) > 0:
            self.calcTop(numStack, opStack)
        return numStack[0]

s = Solution()
ret = s.calculate("1*2-3/4+5*6-7*8+9/10")
2 - 0 + 30 - 56 + 0
print(ret)



        
            