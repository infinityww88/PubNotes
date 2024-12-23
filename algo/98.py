class Solution:
    def minVal(self, root):
        while root.left != None:
            root = root.left
        return root.val
    def maxVal(self, root):
        while root.right != None:
            root = root.right
        return root.val
    def isValidBST(self, root):
        if root.left == None and root.right == None:
            return True
        elif root.left == None and root.right != None:
            return self.isValidBST(root.right) and root.val < self.minVal(root.right)
        elif root.left != None and root.right == None:
            return self.isValidBST(root.left) and root.val > self.maxVal(root.left)
        else:
            return self.isValidBST(root.left) and self.isValidBST(root.right) and root.val > self.maxVal(root.left) and root.val < self.minVal(root.right)
