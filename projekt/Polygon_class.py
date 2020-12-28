class Polygon:
    def __init__(self, vertices): #wierzchołki są zadawane w lewa strone
        self.vertices = self.__sorted_vertices(vertices)
        self.bottom_point_index = 0 #index
        self.top_point_index = self.__top_point() #index
        self.triangles = set()
        self.chain = self.__get_chain()

    def __sorted_vertices(self, vertices):
        index = 0
        for i in range(len(vertices)):
            current = vertices[index].point
            candidate = vertices[i].point
            if candidate.y < current.y:
                index = i
            elif candidate.y == current.y and candidate.x < current.x:
                index = i
        return vertices[i:] + vertices[:i]

    def __top_point(self):
        index = 0
        for i in range(len(self.vertices)):
            current = self.vertices[index].point
            candidate = self.vertices[i].point
            if candidate.y > current.y:
                index = i
            elif candidate.y == current.y and candidate.x < current.x:
                index = i
        return index

    def __get__chain(self):
        C = [1 for _ in range len(self.vertices)]
        i = 0
        while self.vertices[i] != self.vertices[self.top_point_index]:
            C[i] = -1
            i += 1
        C[0] = 0
        C[self.top_point_index] = 0

    def add_triangle(self, triangle):
        self.triangles.add(triangle)

    def __is_y_monotone(self):
        V = self.vertices
        for i in range(self.top_point_index, len(V)):
            if V[(i+1) % len(V)].point.y > V[i % len(V)].point.y:
                return False
        for i in range(self.top_point_index):
            if V((i+1) % len(V)).point.y < V[i % len(V)].point.y:
                return False
        return True
