class Solution:
    def maxProfit(self, prices: list[int]):
        n = len(prices)
        j = 0
        profit = 0
        while j < n:
            while j + 1 < len(prices) and prices[j + 1] <= prices[j]:
                j += 1
            if j + 1 >= len(prices):
                break
            k = j
            while k + 1 < len(prices) and prices[k + 1] >= prices[k]:
                k += 1

            profit += prices[k] - prices[j]
            j = k + 1
        return profit