from projekt.point import Point


class Vertex:
    def __init__(self, point: Point):
        self.point = point
        self.triangles = set([])
        self.sides = set([])

    def __eq__(self, other):
        return isinstance(other, Vertex) and self.point == other.point

    def __hash__(self):
        return hash(self.point)

    def __gt__(self, other):
        if not isinstance(other, Vertex):
            return False
        if self.point.x < other.point.x:
            return True
        return False

    def __str__(self):
        return self.point.to_tuple()

    def add_triangle(self, triangle):
        self.triangles.add(triangle)

    def remove_triangle(self, triangle):
        if triangle in self.triangles:
            self.triangles.remove(triangle)

    def add_side(self, side):
        self.sides.add(side)

    def get_degree(self):
        return len(self.sides)
