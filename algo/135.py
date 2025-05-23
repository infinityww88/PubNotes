class Solution:
    def candy(self, ratings) -> int:
        n = len(ratings)
        candies = [1] * n
        for i in range(n - 1):
            if ratings[i] < ratings[i+1]:
                candies[i+1] = candies[i] + 1
        for i in range(n-1, 0, -1):
            if ratings[i-1] > ratings[i]:
                if candies[i-1] < candies[i] + 1:
                    candies[i-1] = candies[i] + 1
        return sum(candies)

s = Solution()
print(s.candy([1, 2, 2]))