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
            letterCnt[ord(s[i])] -= 1   # 需要的字符减少一个
            # 获取后，这个字符需要的个数如果 >= 0，说明它是真正需要的那些字符，将 cnt + 1
            if letterCnt[ord(s[i])] >= 0:   # 如果字符 s[i] 的需求还没满足，说明刚才获取的字符是必需的，因此 cnt + 1
                cnt += 1
            # cnt == len(t) 说找到一个覆盖子串
            while cnt == len(t):
                # 统计最小窗口，如果当前窗口更小，则更新 min window
                if minLen > i - left + 1:
                    minLen = i - left + 1
                    minLeft = left
                # 窗口即将离开 left，获取的反操作，释放字符，将相应的需要的字符个数 + 1，因为它被释放了，窗口中又缺这个字符了
                letterCnt[ord(s[left])] += 1    # s[left] 字符移出窗口，它的需求又增加了一个
                # 释放后，如果需要字符个数 > 0，说明它是真正需要的（或者又开始需要它了）。那些不需要的字符，获取和释放，个数最高就是 0，不可能大于 0
                if letterCnt[ord(s[left])] > 0: # 只有 letterCnt 中的字符技术 > 0 才说明这个字符是被需要的，是不够的，此时移除之，才可以将 cnt - 1。letterCnt 记录的不仅是 t 需要的字符数，而是所有 128 个 asc 字符，但是其他字符的计数默认是 0，既不需要。因此移入移出的字符还包括其他的 asc 字符。但是非 t 中的字符移入是 letterCnt 会减一，移出时又会加一，因此非 t 中的字符的 letterCnt 不会超过 0. 但是 t 中字符因为在第一个 for 循环中被统计技术，它的 letterCnt 是大于 0 的，因此通过 letterCnt 是否大于 0 就可以判断移入移出的字符是否应该更新 cnt 了。
                    cnt -= 1
                # 释放字符后，窗口左边右移
                left += 1
        return "" if minLeft == -1 else s[minLeft:minLeft+minLen]

s = Solution()
a = "dacbbaca"
b = "aba"
ret = s.minWindow(a, b)
print(ret)
