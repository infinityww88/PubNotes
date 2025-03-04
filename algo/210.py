from typing import List

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        graph = [[] for i in range(numCourses)]
        head = set(range(numCourses))
        indegree = [0 for i in range(numCourses)]
        for p in prerequisites:
            if p[0] == p[1]:
                return False
            if p[0] in head:
                head.remove(p[0])
            graph[p[1]].append(p[0])
            indegree[p[0]] += 1
        visit = set()
        order = []
        while head:
            t = set()
            for n in head:
                visit.add(n)
                order.append(n)
                for k in graph[n]:
                    if k in visit:
                        return []
                    indegree[k] -= 1
                    if indegree[k] == 0:
                        t.add(k)
            head = t
        return order if len(visit) == numCourses else []

s = Solution()
ret = s.findOrder(4, [[1,0],[2,0],[3,1],[3,2]])
print(ret)