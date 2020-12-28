from projekt.Vertex_class import *
from projekt.Point_class import *
from projekt.Triangle_class import *
from projekt.main import *

class Polygon:
    def __init__(self, vertices): #wierzchołki są zadawane w lewa strone
        self.vertices = self.__sorted_vertices(vertices)
        self.bottom_point_index = 0 #index
        self.top_point_index = self.__top_point() #index
        self.triangles = set()
        self.chain = self.__get_chain()
        self.scenes = [] #puste
        self.sides = []
        for i in range(len(self.vertices)):
            self.sides.append([(self.vertices[i].point.x, self.vertices[i].point.y),
                               (self.vertices[(i + 1) % len(self.vertices)].point.x,
                                self.vertices[(i + 1) % len(self.vertices)].point.y)])

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

    def __get_chain(self):
        C = [1 for _ in range(len(self.vertices))]
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

    #moze warto bedzie tu dodac epsilon
    def __classify_vertices(self, epsilon = 0):
        #kolory opisane ponizej do pozniejszej wizualizacji
        classification = {
            # 'limegreen'
            'poczatkowe': [],
            # 'red'
            'koncowe': [],
            # 'mediumblue'
            'laczace': [],
            # 'lightsteelblue'
            'dzielace': [],
            # 'sienna'
            'prawidlowe': []
        }

        V = self.vertices
        n = len(V)

        for i in range(n):
            p, q, r = V[(i-1) % n].point, V[i % n].point, V[(i+1) % n].point
            diff = (p.y - q.y, r.y - q.y)
            d = Point.det(p, q, r)
            if diff[0] > 0 and diff[1] > 0:  # oba punkty są powyzej
                if d > epsilon:  # phi > pi / clockwise
                    classification['laczace'].append(q)
                    continue
                elif d < epsilon:  # phi < pi / counterclockwise
                    classification['koncowe'].append(q)
                    continue
            elif diff[0] < 0 and diff[1] < 0:  # oba punkty są ponizej
                if d > epsilon:  # phi > pi
                    classification['dzielace'].append(q)
                    continue
                elif d < epsilon:  # phi < pi
                    classification['poczatkowe'].append(q)
                    continue
            else:  # prawidlowy
                classification["prawidlowe"].append(q)
        self.scenes.append(Scene(points= [PointsCollection([(p.x,p.y) for p in classification['poczatkowe']], color = 'limegreen'),
                                          PointsCollection([(p.x,p.y) for p in classification['koncowe']], color = 'red'),
                                          PointsCollection([(p.x,p.y) for p in classification['laczace']], color = 'mediumblue'),
                                          PointsCollection([(p.x,p.y) for p in classification['dzielace']], color = 'lightsteelblue'),
                                          PointsCollection([(p.x,p.y) for p in classification['prawidlowe']], color = 'sienna')],
                                 lines = [LinesCollection(self.sides)]))

    def __triangulate(self):
        if not self.__is_y_monotone():
            print("BLAD W __triangulate()") #TODO pozniej usunac
            return
        V = sorted([[self.vertices[i], self.chain[i]] for i in range(len(self.vertices))], key = lambda v: v[0].point.y)

        def belongs(i_p, i_q, i_r) -> bool:
            p = V[i_p][0].point
            q = V[i_q][0].point
            r = V[i_r][0].point

            if V[i_r][1] == 1:
                return Point.orientation(p, q, r) > 0
            else:
                return Point.orientation(p, q, r) < 0

        S = [0,1] #STACK
        for i in range(2,n):
            if V[i][1] == V[S[-1]][1] or V[i][1] == 0 or V[S[-1]][1] == 0:
                nS = []
                while len(S) > 1:
                    if belongs(S[-2], S[-1], i):
                        self.add_triangle(V[i][0], V[S[-1]][0], V[S[-2]][0])
                        S.pop()
                    else:
                        nS.append(S.pop())
                nS.append(S.pop())
                nS.reverse()
                nS.append(i)
                S = nS
            else:
                l = len(S)
                ve = S[-1]
                for j in range(l-1):
                    self.add_triangle(V[i][0], V[S[-1]][0], V[S[-2]][0])
                    S.pop() #v
                S = [ve, i]

    def actions(self):
        self.__classify_vertices()
