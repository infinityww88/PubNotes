class Solution:
    def sortedListToBST(self, head):
        if head == None:
            return None
        dumpNode = ListNode(0, head)
        p0, p, q = dumpNode, head, head
        while q != None and q.next != None:
            p0 = p
            p = p.next
            q = q.next.next
        p0.next = None
        root = TreeNode(p.val, self.sortedListToBST(dumpNode.next), self.sortedListToBST(p.next))
        return root
        