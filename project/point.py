import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    @staticmethod
    def det(p, q, r):
        return (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

    @staticmethod
    def orientation(p, q, r, epsilon=0):
        d = Point.det(p, q, r)
        if d > epsilon:
            return 1  # clockwise
        elif d < (-1) * epsilon:
            return -1  # counterclockwise
        else:
            return 0  # collinear"

    @staticmethod
    def distance(p, q):
        return np.sqrt((p.x - q.x)**2 + (p.y - q.y)**2)

    def to_tuple(self):
        return self.x, self.y

    @staticmethod
    def to_line(p, q):
        return [p.to_tuple(), q.to_tuple()]

