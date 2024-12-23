class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reorderList(self, head):
        """
        Do not return anything, modify head in-place instead.
        """
        dumb = ListNode(0, head)
        p0, p, q = dumb, head, head
        while q and q.next:
            p0 = p0.next
            p = p.next
            q = q.next.next
        p0.next = None
        dumb.next = None
        while p:
            t = p.next
            p.next = dumb.next
            dumb.next = p
            p = t
        head1 = dumb.next
        dumb.next = None
        p = dumb
        while head and head1:
            p.next = head
            head = head.next
            p = p.next
            p.next = head1
            head1 = head1.next
            p = p.next
        if head:
            p.next = head
        else:
            p.next = head1


