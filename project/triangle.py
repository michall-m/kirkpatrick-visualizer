from point import Point
from side import Side
from vertex import Vertex


class Triangle:
    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex, polygon=None):
        self.vertices = set([v1, v2, v3])
        self.children = set([])
        self.polygon = polygon
        for v in [v1, v2, v3]:
            v.add_triangle(self)
        self.sides = set([Side(v1, v2), Side(v2, v3), Side(v3, v1)])
        for s in list(self.sides):
            s.add_triangle(self)

    def __eq__(self, other):
        return isinstance(other, Triangle) and self.vertices == other.vertices

    def __hash__(self):
        h = list(self.vertices)
        return h[0].__hash__() * h[1].__hash__() * h[2].__hash__()

    def to_list(self):
        vertices = list(self.vertices)
        sides = []
        for i in range(3):
            sides.append(Point.to_line(vertices[i].point, vertices[(i + 1) % 3].point))
        return sides

    def add_child(self, triangle):
        self.children.add(triangle)

    def is_in_triangle(self, p: Point):
        a, b, c = [po.point for po in list(self.vertices)]
        v0 = [c.x - a.x, c.y - a.y]
        v1 = [b.x - a.x, b.y - a.y]
        v2 = [p.x - a.x, p.y - a.y]
        cross = lambda u, v: u[0] * v[1] - u[1] * v[0]
        u = cross(v2, v0)
        v = cross(v1, v2)
        d = cross(v1, v0)
        if d < 0:
            u, v, d = -u, -v, -d
        return u >= 0 and v >= 0 and (u + v) <= d

    @property
    def is_leaf(self):
        return self.polygon is not None

    @staticmethod
    def do_overlap(first, second):
        for fs in list(first.sides):
            for ss in list(second.sides):
                c = False
                for v1 in fs.vertices:
                    for v2 in ss.vertices:
                        if v1 == v2:
                            c = True
                if c:
                    continue
                if Side.do_intersect(fs, ss):
                    return True
        for v in list(first.vertices):
            if v not in second.vertices and second.is_in_triangle(v.point):
                return True
        for v in list(second.vertices):
            if v not in first.vertices and first.is_in_triangle(v.point):
                return True
        return False
