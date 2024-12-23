class MinStack:

    def __init__(self):
         self.stk = []
         self.minStk = []

    def push(self, val: int) -> None:
        if not self.stk:
            self.stk.append(val)
            self.minStk.append(val)
        else:
            self.stk.append(val)
            if val < self.minStk[-1]:
                self.minStk.append(val)

    def pop(self) -> None:
        val = self.stk.pop()
        if self.stk[-1] < self.minStk[-1]:
            self.minStk.pop()

    def top(self) -> int:
        return self.stk[-1]

    def getMin(self) -> int:
        return self.minStk[-1]

obj = MinStack()
obj.push(-2)
obj.push(0)
obj.push(-1)
print(obj.getMin())
print(obj.top())
print(obj.pop())
print(obj.getMin())