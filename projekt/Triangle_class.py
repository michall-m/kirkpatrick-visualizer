from projekt.Vertex_class import Vertex


class Triangle:
    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex, children=[], polygon=None):
        self.vertices = {v1, v2, v3}
        self.children = children
        self.polygon = polygon

    def __eq__(self, other):
        return isinstance(other, Triangle) and self.vertices == other.vertices

    def __hash__(self):
        h = list(self.vertices)
        return hash((h[0], h[1], h[2]))

    @property
    def is_leaf(self):
        return self.polygon is not None
