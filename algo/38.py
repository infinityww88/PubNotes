class Solution:
    def countAndSay(self, n: int) -> str:
        arr = ["1"]
        arr0 = []
        for i in range(1, n):
            j, k = 0, 1
            while j < len(arr):
                while k < len(arr) and arr[k] == arr[j]:
                        k += 1
                n = k - j
                arr0.append(str(n))
                arr0.append(arr[j])
                j = k
            arr, arr0 = arr0, arr
            arr0.clear()
        return "".join(arr)

s = Solution()
ret = s.countAndSay(4)
print(ret)