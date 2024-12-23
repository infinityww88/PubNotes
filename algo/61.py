class Solution:
    def rotateRight(self, head, k: int):
        p = head
        tail = None
        n = 0
        while p:
            n += 1
            tail = p
            p = p.next
        s = k % n
        if s == 0:
            return head
        dumb = ListNode(0, head)
        p0, p = dumb, head
        for i in range(s):
            p0 = p0.next
            p = p.next
        p0.next = None
        tail.next = head
        head = p
        return head
