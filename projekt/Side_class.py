from projekt import *
from projekt.Vertex_class import Vertex

class Side:
    def __init__(self, v1: Vertex, v2: Vertex):
        self.vertices = set([v1, v2])
        self.triangles = set()
        for v in self.vertices:
            v.add_side(self)
    def __eq__(self, other):
        return isinstance(other, Side) and self.vertices == other.vertices

    def __hash__(self):
        v_list = list(self.vertices)
        return v_list[0].__hash__() * v_list[1].__hash__()

    def add_triangle(self, triangle):
        self.triangles.add(triangle)

    def get_another_vertice(self, this):
        ver = list(self.vertices)
        if this == ver[0]:
            return ver[1]
        return ver[0]

    def to_list(self):
        return [v.point.to_tuple() for v in self.vertices]