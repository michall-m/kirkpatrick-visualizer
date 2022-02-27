from functools import cmp_to_key
from point import Point





def graham_scan(vertices, e=0):
    most_left = min(vertices, key=lambda v: (v.point.y, v.point.x))

    def is_collinear(a, b, c, e=e):
        return Point.orientation(a.point, b.point, c.point, epsilon=e) == 0

    def sorting_func(b, c):
        p, q, r = most_left.point, b.point, c.point
        if b == c:
            return 0
        orient = Point.orientation(p, q, r, epsilon=e)
        if orient == 1:
            return 1
        if orient == -1:
            return -1
        if Point.distance(p, q) < Point.distance(p, r):
            return -1
        return 1

    def del_collinear(A):
        n = len(A) - 1
        i, j = 1, 2
        while j <= n:
            if is_collinear(most_left, A[i], A[j]):
                del A[i]
                n -= 1
            else:
                i += 1
                j += 1

    def convex_hull(P):
        n = len(sorted_points)
        c_vertices = [P[i] for i in range(3)] + [None for _ in range(3, n)]
        i = 3
        t = 2
        while i < n:
            if Point.orientation(P[i].point, c_vertices[t - 1].point, c_vertices[t].point) == -1:
                t += 1
                c_vertices[t] = P[i]
                i += 1
            else:
                t -= 1
        return c_vertices[:t + 1]

    sorted_points = sorted(vertices, key=cmp_to_key(sorting_func))
    del_collinear(sorted_points)

    return convex_hull(sorted_points)
