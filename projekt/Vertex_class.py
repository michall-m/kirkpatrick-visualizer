from projekt.Point_class import Point


class Vertex:
    def __init__(self, point: Point):
        self.point = point
        self.triangles = []

    def add_triangle(self, triangle):
        self.triangles.append(triangle)

    #zastanowić się nad tym czy powinno się jeszcze triangles porownywac
    def __eq__(self, other):
        return isinstance(other, Vertex) and self.point == other.point

    def __hash__(self):
        return hash(self.point)
