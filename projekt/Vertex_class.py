from projekt.Point_class import Point


class Vertex:
    def __init__(self, point: Point):
        self.point = point
        self.triangles = set()
        self.sides = set()



    #zastanowić się nad tym czy powinno się jeszcze triangles porownywac
    def __eq__(self, other):
        return isinstance(other, Vertex) and self.point == other.point

    def __hash__(self):
        return hash(self.point)

    def __str__(self):
        return self.point.to_tuple()

    def add_triangle(self, triangle):
        self.triangles.add(triangle)

    def add_side(self, side):
        self.sides.add(side)

    def get_degree(self):
        return len(self.sides)

