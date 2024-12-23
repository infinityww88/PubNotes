class Solution:
    def canCompleteCircuit(self, gas, cost):
        n = len(gas)
        i = 0
        while i < n:
            tank = 0
            current = i
            stations = 0
            while tank + gas[current] >= cost[current]:
                tank += gas[current] - cost[current]
                current = (current + 1) % n
                stations += 1
                if stations == n: return i
            if current < i:
                break
            else:
                i = current + 1
        return -1

s = Solution()
ret = s.canCompleteCircuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
print(ret)