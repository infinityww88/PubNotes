class Solution:
    def minWindow(self, s: str, t: str) -> str:
        letterCnt = [0] * 128
        left, cnt, minLeft, minLen = 0, 0, -1, 1000000
        # letterCnt 每个字符需要的个数，t 里面真正需要的字符累加计数，其他字符不需要默认需要0个
        for c in t:
            letterCnt[ord(c)] += 1
        for i in range(len(s)):
            # 每次扫描 s 中的一个字符，都是在“获取”需要的字符，获取后，从“需要每个字符个数记录” letterCnt 中给这个字符需要的个数减 1
            # 不是真正需要的字符会变成负数值，一样是记录需要的个数，只是需要负数个
            letterCnt[ord(s[i])] -= 1
            # 获取后，这个字符需要的个数如果 >= 0，说明它是真正需要的那些字符，将 cnt + 1
            if letterCnt[ord(s[i])] >= 0:
                cnt += 1
            # cnt == len(t) 说找到一个覆盖子串
            while cnt == len(t):
                # 统计最小窗口
                if minLen > i - left + 1:
                    minLen = i - left + 1
                    minLeft = left
                # 窗口即将离开 left，获取的反操作，释放字符，将相应的需要的字符个数 + 1，因为它被释放了，窗口中又缺这个字符了
                letterCnt[ord(s[left])] += 1
                # 释放后，如果需要字符个数 > 0，说明它是真正需要的（或者又开始需要它了）。那些不需要的字符，获取和释放，个数最高就是 0，不可能大于 0
                if letterCnt[ord(s[left])] > 0:
                    cnt -= 1
                # 释放字符后，窗口左边右移
                left += 1
        return "" if minLeft == -1 else s[minLeft:minLeft+minLen]

s = Solution()
a = "dacbbaca"
b = "aba"
ret = s.minWindow(a, b)
print(ret)
