class Solution:
    def dfs(self, root, targetSum):
        self.path.append(root.val)
        targetSum -= root.val
        if root.left == None and root.right == None and targetSum == 0:
            self.ret.append(list(self.path))
            self.path.pop()
            return
        if root.left:
            self.dfs(root.left, targetSum)
        if root.right:
            self.dfs(root.right, targetSum)
        self.path.pop()
        
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        if root == None:
            return []
        self.path = []
        self.ret = []
        self.dfs(root, targetSum)