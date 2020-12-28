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