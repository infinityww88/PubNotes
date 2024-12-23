class Solution:
    def maximumSwap(self, num: int) -> int:
        strval = list(str(num))
        n = len(strval)
        maxIdx = n - 1
        finalIdx = -1
        candidateIdx = -1
        maxNum = strval[-1]
        for i in range(n-2, -1, -1):
            num = strval[i]
            if num > maxNum:
                maxIdx = i
                maxNum = strval[maxIdx]
            elif num < maxNum:
                candidateIdx = i
                finalIdx = maxIdx
        if candidateIdx >= 0:
            strval[candidateIdx], strval[finalIdx] = strval[finalIdx], strval[candidateIdx]
        return int("".join(strval))

print(Solution().maximumSwap(2736))
