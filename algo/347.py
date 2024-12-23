import heapq

class Solution:
    def topKFrequent(self, nums, k):
        count = {}
        for i in nums:
            if i not in count:
                count[i] = 0
            count[i] += 1
        heap = []
        for i, item in enumerate(count.items()):
            if i < k:
                heapq.heappush(heap, (item[1], item[0]))
            else:
                heapq.heappushpop(heap, (item[1], item[0]))
        return [i[1] for i in heap]

s = Solution()
ret = s.topKFrequent([1], 1)
print(ret)