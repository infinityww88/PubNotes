from typing import Optional
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

import math

class Solution:
    def dfs(self, root: Optional[TreeNode]) -> int:
        if root == None:
            return 0
        l = self.dfs(root.left)
        r = self.dfs(root.right)
        m = max(root.val, root.val + l, root.val + r)
        self.maxSum = max(self.maxSum, m)
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.maxSum = -math.inf
        self.dfs(root)
        return self.maxSum