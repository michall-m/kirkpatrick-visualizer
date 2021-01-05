from projekt.Vertex_class import Vertex
from projekt.Point_class import Point
from projekt.Side_class import Side


class Triangle:
    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex, children=[], polygon=None):
        self.vertices = set([v1, v2, v3])
        self.children = children
        self.polygon = polygon
        for v in [v1,v2,v3]:
            v.add_triangle(self)
        self.sides = set([Side(v1,v2), Side(v2, v3), Side(v3, v1)])
        for s in list(self.sides):
            s.add_triangle(self)
        #for v in self.vertices:
        #    v.add_triangle(self)


    def __eq__(self, other):
        return isinstance(other, Triangle) and self.vertices == other.vertices

    def __hash__(self):
        h = list(self.vertices)
        return h[0].__hash__() * h[1].__hash__() * h[2].__hash__()

    def to_list(self):
        vertices = list(self.vertices)
        sides = []
        for i in range(3):
            sides.append(Point.to_line(vertices[i].point, vertices[(i+1)%3].point))
        return sides


    @property
    def is_leaf(self):
        return self.polygon is not None
