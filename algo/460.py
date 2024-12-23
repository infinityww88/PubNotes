'''
dict[key, node] + dict[freq, doublelinkedlist[node]]
freqListMap 记录 freq 对应的 LRU 双向列表队列
node 中记录 key 和 freq
minFreq 总是记录 freq 最小的非空 node 队列，移除时先从这个列表中删除末端元素
新加元素总是 minFreq = 1，即使 freq = 2， 3， 4 是空，freq = 5 非空也没关系
当 minFreq 队列移除末端元素后队列变空，minFreq 直接 +1，因为：
1 如果 LFU 未满，则不会移除元素，只会将元素移动到下一个 freq，因此 minFreq +=1 直接指向下一个最小频率队列
2 如果 LFU 已经满，移除元素后，即使 minFreq += 1，新入元素也会将 minFreq 设置为 1
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
    
class LFUCache:

    def __init__(self, capacity: int):
        self.freqListMap = {}
        self.nodeMap = {}
        self._minFreq = 1
        self.capacity = capacity
        self.size = 0
    
    def _update(self, node):
        node.remove()
        if self._minFreq == node.freq and self.freqListMap[node.freq].empty():
            self._minFreq += 1
        node.freq += 1
        
        if node.freq not in self.freqListMap:
            self.freqListMap[node.freq] = DLinkedList()
        self.freqListMap[node.freq].pushHead(node)

    def get(self, key: int) -> int:
        if key not in self.nodeMap:
            return -1
        node = self.nodeMap[key]
        self._update(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key not in self.nodeMap:
            node = ListNode(key, value)
            if self.size == self.capacity:
                evictNode = self.freqListMap[self._minFreq].popTail()
                del self.nodeMap[evictNode.key]
                self.size -= 1

            self.nodeMap[key] = node
            if node.freq not in self.freqListMap:
                self.freqListMap[node.freq] = DLinkedList()
            self.freqListMap[node.freq].pushHead(node)

            self._minFreq = 1
            self.size += 1
        else:
            node = self.nodeMap[key]
            node.val = value
            self._update(node)

lfu = LFUCache(2)
lfu.put(1, 1)   
lfu.put(2, 2)   
print(lfu.get(1))
                 
lfu.put(3, 3)   
                 
print(lfu.get(2))    
print(lfu.get(3))    
                 
lfu.put(4, 4)   
                 
print(lfu.get(1))
print(lfu.get(3))
print(lfu.get(4))