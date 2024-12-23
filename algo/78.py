from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        record = [[] for i in range(n+1)]
        record[0] = [[]]
        for i in range(1, n+1):
            for j in range(min(i, n), 0, -1):
                record[j].extend([i] + r for r in record[j-1])
        return record[k]