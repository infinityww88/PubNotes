# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def sortList(self, head):
        if not head.next:
            return head
        dumb = ListNode(0, head)
        p0, p, q = dumb, head, head
        while q and q.next:
            p0 = p0.next
            p = p.next
            q = q.next.next
        p0.next = None
        head = self.sortList(head)
        head1 = self.sortList(p)
        p = dumb
        while head and head1:
            if head.val < head1.val:
                p.next = head
                head = head.next
            else:
                p.next = head1
                head1 = head1.next
            p = p.next
        if head:
            p.next = head
        else:
            p.next = head1
        return dumb.next
        