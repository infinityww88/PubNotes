class Solution:
    def nextGreaterElement(self, nums1: list[int], nums2: list[int]) -> list[int]:
        d: dict[int, int] = {}
        for i,v in enumerate(nums1):
            d[v] = i
        stk: list[int] = []
        ret = [-1] * len(nums1)
        for i, v in enumerate(nums2):
            while stk and nums2[stk[-1]] < v:
                t = nums2[stk[-1]]
                if t in d:
                    ret[d[t]] = v
                stk.pop()
            stk.append(i)
        return ret

s = Solution()
nums1 = [2, 4]
nums2 = [1, 2, 3, 4]
ret = s.nextGreaterElement(nums1, nums2)
print(ret)