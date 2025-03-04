from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = [[] for i in range(numCourses)]
        head = set(range(numCourses))
        indegree = [0 for i in range(numCourses)]
        for p in prerequisites:
            if p[0] == p[1]:
                return False
            if p[1] in head:
                head.remove(p[1])
            graph[p[0]].append(p[1])
            indegree[p[1]] += 1
        visit = set()
        while head:
            t = set()
            for n in head:
                visit.add(n)
                for k in graph[n]:
                    if k in visit:
                        return False
                    indegree[k] -= 1
                    if indegree[k] == 0:
                        t.add(k)
            head = t
        return len(visit) == numCourses

s = Solution()
print(s.canFinish(2, [[1, 0]]))