class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        if len(prices) <= 1:
            return 0
        record = [0] * len(prices)
        maxProfit = 0
        maxPrice = prices[-1]
        for i in range(len(prices)-2, -1, -1):
            if prices[i] >= maxPrice:
                maxPrice = prices[i]
            else:
                profit = maxPrice - prices[i]
                maxProfit = max(profit, maxProfit)
            record[i] = maxProfit

        record1 = [0] * len(prices)
        maxProfit = 0
        minPrice = prices[0]
        for i in range(0, len(prices)-1):
            if prices[i] <= minPrice:
                minPrice = prices[i]
            else:
                profit = prices[i] - minPrice
                maxProfit = max(profit, maxProfit)
            record1[i] = maxProfit
        
        maxProfit = 0
        for i in range(1, len(record1)-1):
            maxProfit = max(maxProfit, record1[i] + record[i+1])
        
        maxProfit = max(maxProfit, max(record))
        maxProfit = max(maxProfit, max(record1))
        
        return maxProfit

s = Solution()
arr = [3,3,5,0,0,3,1,4]
ret = s.maxProfit(arr)
print(ret)
        