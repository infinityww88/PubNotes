class Solution:
    def simplifyPath(self, path: str) -> str:
        ret = []
        for i in path.split("/"):
            if i == "" or i == ".":
                continue
            elif i == "..":
                if ret:
                    ret.pop()
            else:
                ret.append(i)
        return "/" + "/".join(ret)

s = Solution()
print(s.simplifyPath("/.../a/../b/c/../d/./"))
            