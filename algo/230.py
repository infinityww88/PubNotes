class Solution:
    def dfs(self, root):
        if root == None:
            return
        self.dfs(root.left)
        if self.k == 0:
            return
        self.k -= 1
        if self.k == 0:
            self.ret = root.val
            return
        self.dfs(root.right)
        
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        self.k = k
        self.dfs(root)
        return self.ret
