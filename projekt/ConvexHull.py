from functools import cmp_to_key
from projekt.Point_class import Point


def comparing_f(a, b, c, e=0):
    p = a.point
    q = b.point
    r = c.point
    if (b == c):
        return 0
        # print ("Equal")
    orient = Point.orientation(p, q, r, epsilon=e)
    # print("a: ", a, "   b: ", b, "   c: ", c, "    orient:",orientation)
    if orient == 1:
        # print("True")
        return 1
    if orient == -1:
        # print("False")
        return -1
    if Point.distance(p, q) < Point.distance(p, r):
        # print("False")
        return -1
    # print("True")
    return 1

def graham_scan(vertices):
    most_left = min(vertices, key=lambda v: (v.point.y, v.point.x))


    def is_collinear(a, b, c, e=0):
        return Point.orientation(a.point, b.point, c.point, epsilon=e) == 0

    def sorting_f(b, c):
        return comparing_f(most_left, b, c)



    s_points = sorted(vertices, key=cmp_to_key(sorting_f))

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

    del_collinear(s_points)

    def convex_hull(P):
        n = len(s_points)
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

    return convex_hull(s_points)
