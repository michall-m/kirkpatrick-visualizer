from projekt.Vertex_class import Vertex
from projekt.Point_class import Point


class Triangle:
    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex, children=[], polygon=None):
        self.vertices = {v1, v2, v3}
        self.children = children
        self.polygon = polygon
        for v in [v1,v2,v3]:
            v.add_triangle(self)


    def __eq__(self, other):
        return isinstance(other, Triangle) and self.vertices == other.vertices

    def __hash__(self):
        h = list(self.vertices)
        return hash((h[0], h[1], h[2]))

    def to_list(self):
        vertices = list(self.vertices)
        sides = []
        for i in range(3):
            sides.append(Point.to_line(vertices[i].point, vertices[(i+1)%3].point))
        return sides


    @property
    def is_leaf(self):
        return self.polygon is not None
