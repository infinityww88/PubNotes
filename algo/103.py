class Solution:
    def zigzagLevelOrder(self, root):
        stack1 = []
        stack2 = []
        ret = []
        toLeft = True
        if root != None:
            stack1.append(root)
        while len(stack1) > 0:
            t = []
            while len(stack1) > 0:
                e = stack1.pop(0)
                t.append(e.val)
                if toLeft:
                    if e.right != None:
                        stack2.append(e.right)
                    if e.left != None:
                        stack2.append(e.left)
                else:
                    if e.left != None:
                        stack2.append(e.left)
                    if e.right != None:
                        stack2.append(e.right)
            toLeft = not toLeft
            ret.append(t)
            stack1, stack2 = stack2, stack1
        return ret

