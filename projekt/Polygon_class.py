from projekt.Vertex_class import *
from projekt.Point_class import *
from projekt.Triangle_class import *
from projekt.main import *
from projekt.helper_functions import *


class Polygon:
    def __init__(self, vertices):  # wierzchołki są zadawane w lewa strone
        self.vertices = self.__sorted_vertices(vertices)
        self.bottom_point_index = 0  # index
        self.top_point_index = self.__top_point()  # index
        self.triangles = set()
        self.chain = self.__get_chain()
        self.scenes = []  # puste
        self.sides = [] #jako listy
        self.__is_triangulated = False
        self.parent = None #dzielimy niemonotoniczny na monotoniczne i one mają ten bazowy jako parent
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
        return vertices[index:] + vertices[:index]

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
        C[0] = -1
        C[self.top_point_index] = 1
        return C

    def add_triangle(self, triangle):
        self.triangles.add(triangle)
        triangle.polygon = self

    def __is_y_monotone(self):
        V = self.vertices
        for i in range(self.top_point_index, len(V)):
            if V[(i + 1) % len(V)].point.y > V[i % len(V)].point.y:
                return False
        for i in range(self.top_point_index):
            if V[(i + 1) % len(V)].point.y < V[i % len(V)].point.y:
                return False
        return True

    # moze warto bedzie tu dodac epsilon
    def __classify_vertices(self, epsilon=0):
        # kolory opisane ponizej do pozniejszej wizualizacji
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

        classified_vertices = {}

        V = self.vertices
        n = len(V)

        for i in range(n):
            p, q, r = V[(i - 1) % n].point, V[i % n].point, V[(i + 1) % n].point
            diff = (p.y - q.y, r.y - q.y)
            d = Point.det(p, q, r)
            if diff[0] > 0 and diff[1] > 0:  # oba punkty są powyzej
                if d > epsilon:  # phi > pi / clockwise
                    classification['laczace'].append(q)
                    classified_vertices[q] = 'laczace'
                    continue
                elif d < epsilon:  # phi < pi / counterclockwise
                    classification['koncowe'].append(q)
                    classified_vertices[q] = 'koncowe'
                    continue
            elif diff[0] < 0 and diff[1] < 0:  # oba punkty są ponizej
                if d > epsilon:  # phi > pi
                    classification['dzielace'].append(q)
                    classified_vertices[q] = 'dzielace'
                    continue
                elif d < epsilon:  # phi < pi
                    classification['poczatkowe'].append(q)
                    classified_vertices[q] = 'poczatkowe'
                    continue
            else:  # prawidlowy
                classification['prawidlowe'].append(q)
                classified_vertices[q] = 'prawidlowe'

        self.scenes.append(
            Scene(points=[PointsCollection([(p.x, p.y) for p in classification['poczatkowe']], color='limegreen'),
                          PointsCollection([(p.x, p.y) for p in classification['koncowe']], color='red'),
                          PointsCollection([(p.x, p.y) for p in classification['laczace']], color='mediumblue'),
                          PointsCollection([(p.x, p.y) for p in classification['dzielace']], color='lightsteelblue'),
                          PointsCollection([(p.x, p.y) for p in classification['prawidlowe']], color='sienna')],
                  lines=[LinesCollection(self.sides)]))
        return classified_vertices

    # TODO n^2 - > n log n, naming conventions, lambdas
    def failedPrepareForTriangulation(self):
        classification = self.__classify_vertices()
        points = self.vertices.copy()
        edges = []
        newEdges = []
        for i in range(len(points)):
            edges.append([points[i - 1], points[i]])
        points.sort(key=(compareKey1), reverse=True)  # TODO lambda
        edges.sort(key=(compareKey2))  # TODO lambda
        broom = []  # miotla, na pozycji 0 ma pomocnika krawedzi, a na pozycji 1 krawedz
        for point in points:
            if classification[point.point] == 'prawidlowe':
                start = binary_searchleftmost(edges, point.point.y, 0, len(edges) - 1)
                if (start == -1):
                    print("Prepare for triangulation error")
                    return None
                for i in range(start, len(edges)):
                    if edges[i][0].point.x == point.point.x:
                        start = i
                        break
                if (edges[start][0].point.y > edges[start][1].point.y):
                    for edge in broom:
                        if edge[1][1].point == point.point:
                            if classification[edge[0].point] == 'laczace':
                                newEdges.append([edge[0], edge[1][1]])
                        broom.remove(edge)
                        break
                    broom.append([point, edges[start]])
                else:
                    if len(broom) == 1:
                        if classification[broom[0][0].point] == 'laczace':
                            newEdges.append([broom[0][0], broom[0][1][1]])
                        broom[0][0] = point
                    else:
                        indeks = 0
                        distance = float('inf')
                        for i in range(len(broom)):
                            curr_dis = ((broom[i][1][0].point.x - broom[i][1][1].point.x) / (
                                    broom[i][1][0].point.y - broom[i][1][1].point.y) *
                                        (point.point.y - broom[i][1][1].point.y) + broom[i][1][1].point.x)
                            curr_dis -= point.point.x
                            curr_dis *= -1
                            type(curr_dis)
                            if curr_dis > 0 and curr_dis < distance:
                                distance = curr_dis
                                indeks = i
                        if classification[broom[indeks][0].point] == 'laczace':
                            newEdges.append([broom[indeks][0], broom[indeks][1][1]])
                        broom[indeks][0] = point
            elif classification[point.point] == 'poczatkowe':
                start = binary_searchleftmost(edges, point.point.y, 0, len(edges) - 1)
                if (start == -1):
                    print("Prepare for triangulation error")
                    return None
                for i in range(start, len(edges)):
                    if edges[i][0].point.x == point.point.x:
                        broom.append([point, edges[i]])
                        break
            elif classification[point.point] == 'koncowe':
                for edge in broom:
                    if edge[1][1].point == point.point:
                        if classification[edge[0].point] == 'laczace':
                            newEdges.append([edge[0], edge[1][1]])
                        broom.remove(edge)
                        break
            elif classification[point.point] == 'dzielace':
                indeks = 0
                distance = float('inf')
                for i in range(len(broom)):
                    curr_dis = ((broom[i][1][0].point.x - broom[i][1][1].point.x) / (
                            broom[i][1][0].point.y - broom[i][1][1].point.y) *
                                (point.point.y - broom[i][1][1].point.y) + broom[i][1][1].point.x)
                    curr_dis -= point.point.x
                    curr_dis *= -1
                    type(curr_dis)
                    if curr_dis > 0 and curr_dis < distance:
                        distance = curr_dis
                        indeks = i
                newEdges.append([point, broom[indeks][0]])
                broom[indeks][0] = point
                start = binary_searchleftmost(edges, point.point.y, 0, len(edges) - 1)
                if (start == -1):
                    print("Prepare for triangulation error")
                    return None
                for i in range(start, len(edges)):
                    if edges[i][0].point.x == point.point.x:
                        broom.append([point, edges[i]])
                        break
            elif classification[point.point] == 'laczace':
                for edge in broom:
                    if edge[1][1].point == point.point:
                        if classification[edge[0].point] == 'laczace':
                            newEdges.append([edge[0], edge[1][1]])
                        broom.remove(edge)
                if len(broom) == 1:
                    if classification[broom[0][0].point] == 'laczace':
                        newEdges.append([broom[0][0], broom[0][1][1]])
                    broom[0][0] = point
                else:
                    indeks = 0
                    distance = float('inf')
                    for i in range(len(broom)):
                        curr_dis = ((broom[i][1][0].point.x - broom[i][1][1].point.x) / (
                                broom[i][1][0].point.y - broom[i][1][1].point.y) *
                                    (point.point.y - broom[i][1][1].point.y) + broom[i][1][1].point.x)
                        curr_dis -= point.point.x
                        curr_dis *= -1
                        type(curr_dis)
                        if curr_dis > 0 and curr_dis < distance:
                            distance = curr_dis
                            indeks = i
                    if classification[broom[indeks][0].point] == 'laczace':
                        newEdges.append([broom[indeks][0], broom[indeks][1][1]])
                    broom[indeks][0] = point
        #        for newEdge in newEdges:
        #           print(newEdge[0].point.x)
        #          print(newEdge[0].point.y)
        #         print(newEdge[1].point.x)
        #        print(newEdge[1].point.y)
        #       print("\n")
        self.scenes.append(Scene(lines=[LinesCollection(self.sides),
                                        LinesCollection([Point.to_line(v[0].point, v[1].point) for v in newEdges],
                                                        color='crimson')]))
        return newEdges

    def PrepareForTriangulation(self):
        classification = self.__classify_vertices()
        points = self.vertices.copy()
        edges = []
        newEdges = []
        for i in range(len(points)):
            edges.append([points[i - 1], points[i]])
        points.sort(key=(compareKey1), reverse=True)  # TODO lambda
        edges.sort(key=(compareKey2))  # TODO lambda
        broom = []  # miotla, na pozycji 0 ma pomocnika krawedzi, a na pozycji 1 krawedz
        for vertex in points:
            if classification[vertex.point] == 'prawidlowe':
                start = binary_searchleftmost(edges, vertex.point.y, 0, len(edges) - 1)
                for i in range(start, len(edges)):
                    if edges[i][0].point.x == vertex.point.x:
                        start = i
                        break
                if (edges[start][0].point.y > edges[start][1].point.y):
                    for edge in broom:
                        if edge[1][1].point == vertex.point:
                            if classification[edge[0].point] == 'laczace':
                                newEdges.append([edge[0], edge[1][1]])
                        broom.remove(edge)
                        break
                    broom.append([vertex, edges[start]])
                else:
                    if len(broom) == 1:
                        if classification[broom[0][0].point] == 'laczace':
                            newEdges.append([broom[0][0], vertex])
                        broom[0][0] = vertex
                    else:
                        indeks = 0
                        distance = float('inf')
                        for i in range(len(broom)):
                            curr_dis = ((broom[i][1][0].point.x - broom[i][1][1].point.x) / (
                                        broom[i][1][0].point.y - broom[i][1][1].point.y) *
                                        (vertex.point.y - broom[i][1][1].point.y) + broom[i][1][1].point.x)
                            curr_dis -= vertex.point.x
                            curr_dis *= -1
                            type(curr_dis)
                            if curr_dis > 0 and curr_dis < distance:
                                distance = curr_dis
                                indeks = i
                        if classification[broom[indeks][0].point] == 'laczace':
                            newEdges.append([broom[indeks][0], vertex])
                        broom[indeks][0] = vertex
            elif classification[vertex.point] == 'poczatkowe':
                start = binary_searchleftmost(edges, vertex.point.y, 0, len(edges) - 1)
                for i in range(start, len(edges)):
                    if edges[i][0].point.x == vertex.point.x:
                        broom.append([vertex, edges[i]])
                        break
            elif classification[vertex.point] == 'koncowe':
                for edge in broom:
                    if edge[1][1].point == vertex.point:
                        if classification[edge[0].point] == 'laczace':
                            newEdges.append([edge[0], edge[1][1]])
                        broom.remove(edge)
                        break
            elif classification[vertex.point] == 'dzielace':
                indeks = 0
                distance = float('inf')
                for i in range(len(broom)):
                    curr_dis = ((broom[i][1][0].point.x - broom[i][1][1].point.x) / (
                                broom[i][1][0].point.y - broom[i][1][1].point.y) *
                                (vertex.point.y - broom[i][1][1].point.y) + broom[i][1][1].point.x)
                    curr_dis -= vertex.point.x
                    curr_dis *= -1
                    type(curr_dis)
                    if curr_dis > 0 and curr_dis < distance:
                        distance = curr_dis
                        indeks = i
                newEdges.append([vertex, broom[indeks][0]])
                broom[indeks][0] = vertex
                start = binary_searchleftmost(edges, vertex.point.y, 0, len(edges) - 1)
                for i in range(start, len(edges)):
                    if edges[i][0].point.x == vertex.point.x:
                        broom.append([vertex, edges[i]])
                        break
            elif classification[vertex.point] == 'laczace':
                for edge in broom:
                    if edge[1][1].point == vertex.point:
                        if classification[edge[0].point] == 'laczace':
                            newEdges.append([edge[0], edge[1][1]])
                        broom.remove(edge)
                if len(broom) == 1:
                    if classification[broom[0][0].point] == 'laczace':
                        newEdges.append([broom[0][0], broom[0][1][1]])
                    broom[0][0] = vertex
                else:
                    indeks = 0
                    distance = float('inf')
                    for i in range(len(broom)):
                        curr_dis = ((broom[i][1][0].point.x - broom[i][1][1].point.x) / (
                                    broom[i][1][0].point.y - broom[i][1][1].point.y) *
                                    (vertex.point.y - broom[i][1][1].point.y) + broom[i][1][1].point.x)
                        curr_dis -= vertex.point.x
                        curr_dis *= -1
                        if curr_dis > 0 and curr_dis < distance:
                            distance = curr_dis
                            indeks = i
                    if classification[broom[indeks][0].point] == 'laczace':
                        newEdges.append([broom[indeks][0], broom[indeks][1][1]])
                    broom[indeks][0] = vertex
        self.scenes.append(Scene(lines=[LinesCollection(self.sides),
                                        LinesCollection([Point.to_line(v[0].point, v[1].point) for v in newEdges],
                                                        color='crimson')]))
        return newEdges


    def __partition_into_monotone_subpolygons(self):
        edges = self.PrepareForTriangulation()
        vertices = {}
        vertices_index = {}
        for v in self.vertices:
            vertices[v] = []
        for i in range(len(self.vertices)):
            vertices_index[self.vertices[i]] = i
        for v1,v2 in edges:     #TODO sort
            if vertices_index[v1] < vertices_index[v2]:
                vertices[v2].append(v1)
            else:
                vertices[v1].append(v2)
        ver = self.vertices.copy()
        e = len(edges)
        subpolygons = []
        diff = 0
        """
        if edges:
            start_i = vertices_index[min(edges[0][0], edges[0][1], key = lambda e: vertices_index[e])]
            ver = ver[start_i:] + ver[:start_i]
            for i in range(len(ver)):
                vertices_index[ver[i]] = i"""
                #to przerobic zeby wystapoealo jakos tak przed 255 linijka

        def new_subpolygon(t, index, ver, vertices, subpolygons, e):
            i = index
            j = index
            first_loop = True
            current_subpolygon_vertices = []
            while(first_loop or (e>0 and ver[j] != t)):
                curr = ver[j]
                if first_loop:
                    first_loop = False
                if not vertices[ver[j]]:
                    j += 1
                else:
                    tmp = vertices[ver[j]][-1]
                    vertices[ver[j]].pop()
                    e, ver = new_subpolygon(ver[j], vertices_index[tmp], ver, vertices, subpolygons, e)
                    j -= len(subpolygons[-1].vertices) - 2
                    ss = j
                    while (ss != len(ver)):
                        vertices_index[ver[ss]] -= len(subpolygons[-1].vertices) - 2
                        ss += 1
                    #current_subpolygon_vertices = current_subpolygon_vertices[:(-1)*(len(subpolygons[-1].vertices)-1)] + [current_subpolygon_vertices[-1]]
            if e == 0:
                current_subpolygon_vertices = [] + ver
            else:
                current_subpolygon_vertices = ver[i:j+1]
            subpolygons.append(Polygon(current_subpolygon_vertices))
            return e-1, ver[:i+1] + ver[j:]
        new_subpolygon(ver[0], 0, ver, vertices, subpolygons, e)
        sd = []
        for sp in subpolygons:
            sd = [] + sd + sp.sides.copy()
            sp.parent = self
            self.scenes.append(Scene(lines = [LinesCollection(sp.sides.copy(), color = 'green')]))
            trl = []
            for tr in sp.triangles:
                trl += tr.to_list()
            self.scenes.append(Scene(lines = [LinesCollection(trl, color = 'crimson')]))
        return subpolygons
        zz = 1



    """
    def __partition_into_monotone_subpolygons(self):
        edges = self.PrepareForTriangulation()
        vertices = {}
        for v in self.vertices:
            vertices[v] = []
        for e1, e2 in edges:
            vertices[e1].append(e2)
            vertices[e2].append(e1)
        for v in self.vertices:
            bottom_point = self.vertices[self.bottom_point_index].point
            vertices[v].sort(key=lambda v: (v.point.x - bottom_point.x) / (
                        v.point.y - bottom_point.y) if v.point.y - bottom_point.y != 0 else float('inf'), reverse=True)


        subpolygons = []
        start_vertex = 0
        ver = self.vertices.copy() #+ self.vertices.copy()
        for i in range(len(ver)):
            v = ver[i]
            if vertices[v]:
                if vertices[v][0] == edges[0][0]:
                    start_vertex = i
                    break
        ver = ver[start_vertex:] + ver[:start_vertex]
        ver += [ver[0]]
        n = len(ver)#/2 + start_vertex
        while()
        
        
        
        
        
        
        def gen_subpolygon(t, index, subpolygons, ver, n, vertices):
            first_loop = True
            i = index
            current_subpolygon_vertices = [ver[i]]
            while((ver[i] != t or first_loop)):
                self.scenes.append(Scene(lines = [LinesCollection(self.sides)], points= [PointsCollection([ver[i].point.to_tuple()], color = 'crimson')]))
                self.scenes.append(Scene(lines = [LinesCollection([Point.to_line(ver[ii].point, ver[(ii+1)%len(ver)].point) for ii in range(len(ver))], color = 'green')], points= [PointsCollection([ver[i].point.to_tuple()], color = 'crimson')]))
                print(ver)
                if first_loop:
                    first_loop = False
                if not vertices[ver[i]]:
                    i += 1
                    i = i
                else: #while
                    next_vertex = vertices[ver[i]].pop()
                    
                    if vertices[next_vertex]:
                        for nv in vertices[next_vertex]:
                            if nv == ver[i]:
                                vertices[next_vertex].remove(ver)
                                break
                    ver = gen_subpolygon(next_vertex, i, subpolygons, ver, n, vertices)
                    teee = 1
                current_subpolygon_vertices.append(ver[i])
            current_subpolygon_vertices.append(t)
            subpolygons.append(Polygon(current_subpolygon_vertices))
            return ver[:index+1]+ver[i:]


        gen_subpolygon(ver[0], 0, subpolygons, ver, n, vertices)
        
        for spol in subpolygons:
            self.scenes.append(Scene(lines = [LinesCollection(spol.sides)]))
        zzz = 100
        """



    def triangulate(self):
        if not self.__is_y_monotone():
            print("BLAD W __triangulate()")  # TODO pozniej usunac
            #raise IOError
            #return
        if self.__is_triangulated:
            return
        if len(self.vertices) < 3:
            return
        V = sorted([[self.vertices[i], self.chain[i]] for i in range(len(self.vertices))], key=lambda v: v[0].point.y)
        if len(V) == 3:
            self.add_triangle(Triangle(V[0][0], V[1][0], V[2][0]))
            return
        def belongs(i_p, i_q, i_r) -> bool:
            p = V[i_p][0].point
            q = V[i_q][0].point
            r = V[i_r][0].point

            if V[i_r][1] == 1:
                return Point.orientation(p, q, r) > 0
            else:
                return Point.orientation(p, q, r) < 0

        S = [0, 1]  # STACK
        n = len(V)

        for i in range(2, n):
            if V[i][1] == V[S[-1]][1] or V[i][1] == 0 or V[S[-1]][1] == 0:
                nS = []
                while len(S) > 1:
                    if belongs(S[-2], S[-1], i):
                        self.add_triangle(Triangle(V[i][0], V[S[-1]][0], V[S[-2]][0]))
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
                for j in range(l - 1):
                    self.add_triangle(Triangle(V[i][0], V[S[-1]][0], V[S[-2]][0]))
                    S.pop()  # v
                S = [ve, i]
        ts = []
        self.scenes.append(Scene(lines = [LinesCollection([tr.to_list()[i] for tr in self.triangles for i in range(3)], color = 'crimson')]))
        self.__is_triangulated = True
        """
        if len(S) > 3:
            tmp_polygon = Polygon([V[s][0] for s in S])
            tmp_polygon.triangulate()
            for tr in list(tmp_polygon.triangles):
                self.add_triangle(tr)
        
        while len(S) > 3:
            for i in range(1,len(S)):
                if Point.orientation(V[S[0]][0].point, V[S[1]][0].point, V[S[2]][0].point) != Point.orientation(V[S[i]][0].point, V[S[i+1]][0].point, V[S[i+2]][0].point):
                    self.add_triangle(Triangle(V[S[0]][0], V[S[1]][0], V[S[2]][0]))
                    S = S[:1] + S[2:]
                    break
                self.add_triangle(Triangle(V[S[0]][0], V[S[1]][0], V[S[2]][0]))
                S = S[:1] + S[2:]
                """
        #if len(S) == 3:
        #    self.add_triangle(Triangle(V[S[0]][0], V[S[1]][0], V[S[2]][0]))


    def __triangulation(self):
        if self.__is_y_monotone():
            self.triangulate()
        else:
            subpolygons = self.__partition_into_monotone_subpolygons()
            for sb in subpolygons:
                sb.triangulate()
                for tr in list(sb.triangles):
                    self.add_triangle(tr)
            self.scenes += sb.scenes
        s = []
        for tr in list(self.triangles):
            s += tr.to_list()
        self.scenes.append(Scene(lines= [LinesCollection(self.sides), LinesCollection(s, color='yellow')]))


    def actions(self):
        self.__triangulation()
        # self.__classify_vertices()
        # self.PrepareForTriangulation()


    def to_scene(self, triangles = False, color = 'dodgerblue', color2 = 'dodgerblue'):
        triangles = []
        for tr in self.triangles:
            triangles += tr.to_list()
        return Scene(lines=[LinesCollection(triangles, color = color2)#,
                            #LinesCollection(self.sides, color = color)
                    ])
