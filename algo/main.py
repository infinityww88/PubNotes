class A:
    def __init__(self, v):
        self.val = v

a = A(10)
a.__dict__["val1"] = 100

print(a.val1)