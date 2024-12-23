'''
一个 dict 记录 key => node（双向链表节点）
一个双向链表用来实现一个双端队列，记录最近使用元素，支持在head插入，在tail删除
分别用两个dumb节点记录head 和 tail，简化双向链表操作
节点可以直接从双向链表中移除
node 记录 key，value，prev，next。之所以要记录 key 是因为当移除最少使用元素时，需要从 nodemap 中移除这个节点，需要从 node 中知道它的 key
双向链表前端表示最新使用的元素，末端表示最少使用的元素。移除最少使用的元素时，移除末端元素，当元素给 get 或 put 时，移动到 head
移除元素时，先从双向链表移除 tail，然后从 nodemap 中移除对应的 key
总而言之，dict[key, node] + doublelinkedlist[node]
'''
class ListNode:
    def __init__(self, key = None, val = None, freq = 1, prev = None, next = None):
        self.key = key
        self.val = val
        self.freq = freq
        self.prev = prev
        self.next = next
    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.prev = self.next = None

class DLinkedList:
    def __init__(self):
        self.head = ListNode()
        self.tail = ListNode()
        self.tail.prev = self.head
        self.head.next = self.tail

    def empty(self):
        return self.head.next == self.tail
    
    def popTail(self):
        if self.empty():
            return
        node = self.tail.prev
        node.remove()
        return node
    
    def pushHead(self, node):
        node.next = self.head.next
        node.prev = self.head
        node.next.prev = node
        node.prev.next = node
    
class LRUCache:

    def __init__(self, capacity: int):
        self.freqList = DLinkedList()
        self.nodeMap = {}
        self.capacity = capacity
        self.size = 0
    
    def get(self, key: int) -> int:
        if key not in self.nodeMap:
            return -1
        node = self.nodeMap[key]
        node.remove()
        self.freqList.pushHead(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key not in self.nodeMap:
            if self.size == self.capacity:
                evictNode = self.freqList.popTail()
                del self.nodeMap[evictNode.key]
                self.size -= 1
            node = ListNode(key, value)
            self.nodeMap[key] = node
            self.freqList.pushHead(node)
            self.size += 1
        else:
            node = self.nodeMap[key]
            node.val = value
            node.remove()
            self.freqList.pushHead(node)
        
lRUCache = LRUCache(2)

'''
lRUCache.put(2, 1)
lRUCache.put(2, 2) 
print(lRUCache.get(2))
lRUCache.put(1, 1) 
lRUCache.put(4, 1) 
print(lRUCache.get(2))
'''

lRUCache.put(1, 1)
lRUCache.put(2, 2) 
print(lRUCache.get(1))
lRUCache.put(3, 3) 
print(lRUCache.get(2))
lRUCache.put(4, 4)
print(lRUCache.get(1))
print(lRUCache.get(3))
print(lRUCache.get(4))