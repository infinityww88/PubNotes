class Solution:
    def dfs(self, root):
        if root == None:
            return
        self.dfs(root.left)
        if self.preNode != None:
            if self.preNode.val > root.val:
                if self.bigNode == None:
                    self.bigNode = self.preNode
                    self.smallNode = root
                else:
                    self.smallNode = root
        self.preNode = root
        self.dfs(root.right)
    def recoverTree(self, root):
        self.preNode = None
        self.bigNode = None
        self.smallNode = None
        self.dfs(root)
        self.bigNode.val, self.smallNode.val = self.smallNode.val, self.bigNode.val