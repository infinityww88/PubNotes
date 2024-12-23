from typing import List

class Solution:
    def maxProfit(self, prices: List[int]):
        n = len(prices)
        j = 0
        profit = 0
        max0 = 0
        max1 = 0
        while j < n:
            while j + 1 < len(prices) and prices[j + 1] <= prices[j]:
                j += 1
            if j + 1 >= len(prices):
                break
            k = j
            while k + 1 < len(prices) and prices[k + 1] >= prices[k]:
                k += 1
            profit = prices[k] - prices[j]
            if profit > max0:
                max0, max1 = profit, max0
            elif profit > max1:
                max1 = profit
            j = k + 1
        return max0 + max1

s = Solution()
arr = [1,2,4,2,5,7,2,4,9,0]
ret = s.maxProfit(arr)
print(ret)
