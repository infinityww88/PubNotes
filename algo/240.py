from typing import List

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        a, b = 0, m-1
        c, d = 0, n-1
        while a <= b and c <= d:
            pass