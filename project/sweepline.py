from project.vertex import Vertex


class Sweepline:
    def __init__(self, helper: Vertex, v1: Vertex, v2: Vertex):
        self.vertices = (v1, v2)
        self.helper = helper

    def __eq__(self, other):
        return self.vertices[0] == other.vertices[0]

    def __gt__(self, other):
        if not isinstance(other, Sweepline):
            return False
        min_x, min_y = self.vertices[0].point.x, self.vertices[0].point.y
        max_x, max_y = other.vertices[0].point.x, other.vertices[0].point.y
        if max_y < min_y:
            min_y, max_y = max_y, min_y
            min_x, max_x = max_x, min_x
            new_x = ((max_x - self.vertices[1].point.x) / (max_y - self.vertices[1].point.y) *
                     (min_y - self.vertices[1].point.y) + self.vertices[1].point.x)
        else:
            new_x = ((max_x - other.vertices[1].point.x) / (max_y - other.vertices[1].point.y) *
                    (min_y - other.vertices[1].point.y) + other.vertices[1].point.x)

        if new_x - min_x > 0:
            return True
        return False
