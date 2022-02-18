from projekt.GUI import *
from projekt.helper_functions import *
from projekt.triangle import *
from math import sqrt

border_triangle_vertices_coords = [(-10, -6), (0, -6 + 10 * sqrt(3)), (10, -6)]


class Polygon:
    def __init__(self, vertices):  # given counter-clockwise
        self.vertices = self.__sorted_vertices(vertices)
        self.bottom_point_index = 0
        self.top_point_index = self.__top_point()
        self.triangles = set()
        self.chain = self.__get_chain()
        self.scenes = []
        self.scene = None #todo del
        self.classification_scene = None
        self.sides = []
        self.__is_triangulated = False
        self.parent = None  # last bigger non-y-monotonic polygon
        self.sub_polygons = []
        self.additional_diagonals = []
        for i in range(len(self.vertices)):
            self.sides.append([(self.vertices[i].point.x, self.vertices[i].point.y),
                               (self.vertices[(i + 1) % len(self.vertices)].point.x,
                                self.vertices[(i + 1) % len(self.vertices)].point.y)])


    def __key(self):
        return tuple(self.vertices)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__key() == other.__key()
        return False

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

    def add_triangle(self, triangle, change=True):
        self.triangles.add(triangle)
        if change:
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

    def __classify_vertices(self, epsilon=0, scenes=False):
        classification = {
            # 'limegreen'
            'start': [],
            # 'red'
            'end': [],
            # 'mediumblue'
            'merge': [],
            # 'lightsteelblue'
            'split': [],
            # 'sienna'
            'regular': []
        }

        classified_vertices = {}

        V = self.vertices
        n = len(V)

        for i in range(n):
            p, q, r = V[(i - 1) % n].point, V[i % n].point, V[(i + 1) % n].point
            diff = (p.y - q.y, r.y - q.y)
            d = Point.det(p, q, r)
            if diff[0] > 0 and diff[1] > 0:  # both points above
                if d > epsilon:  # phi > pi / clockwise
                    classification['merge'].append(q)
                    classified_vertices[q] = 'merge'
                    continue
                elif d < epsilon:  # phi < pi / counterclockwise
                    classification['end'].append(q)
                    classified_vertices[q] = 'end'
                    continue
            elif diff[0] < 0 and diff[1] < 0:  # both points below
                if d > epsilon:  # phi > pi
                    classification['split'].append(q)
                    classified_vertices[q] = 'split'
                    continue
                elif d < epsilon:  # phi < pi
                    classification['start'].append(q)
                    classified_vertices[q] = 'start'
                    continue
            else:  # regular
                classification['regular'].append(q)
                classified_vertices[q] = 'regular'

        self.classification_scene = Scene(points=[PointsCollection([(p.x, p.y) for p in classification['start']], color='limegreen'),
                          PointsCollection([(p.x, p.y) for p in classification['end']], color='red'),
                          PointsCollection([(p.x, p.y) for p in classification['merge']], color='mediumblue'),
                          PointsCollection([(p.x, p.y) for p in classification['split']], color='lightsteelblue'),
                          PointsCollection([(p.x, p.y) for p in classification['regular']], color='sienna')],
                  lines=[LinesCollection(self.sides),
                         LinesCollection([[border_triangle_vertices_coords[i % 3], border_triangle_vertices_coords[(i + 1) % 3]] for i in range(3)], color='navy')])
        return classified_vertices

    def prepare_for_triangulation(self):
        classification = self.__classify_vertices()
        points = self.vertices.copy()
        edges = []
        new_edges = []
        for i in range(len(points)):
            edges.append([points[i - 1], points[i]])
        points.sort(key=lambda x: x.point.y, reverse=True)
        edges.sort(key=lambda x: x[0].point.y)
        sweepline = []  # miotla, na pozycji 0 ma pomocnika krawedzi, a na pozycji 1 krawedz
        for vertex in points:
            if classification[vertex.point] == 'regular':
                start = leftmost_binary_search(edges, vertex.point.y, 0, len(edges) - 1)
                for i in range(start, len(edges)):
                    if edges[i][0].point.x == vertex.point.x:
                        start = i
                        break
                if (edges[start][0].point.y > edges[start][1].point.y):
                    for edge in sweepline:
                        if edge[1][1].point == vertex.point:
                            if classification[edge[0].point] == 'merge':
                                new_edges.append([edge[0], edge[1][1]])
                        sweepline.remove(edge)
                        break
                    sweepline.append([vertex, edges[start]])
                else:
                    if len(sweepline) == 1:
                        if classification[sweepline[0][0].point] == 'merge':
                            new_edges.append([sweepline[0][0], vertex])
                        sweepline[0][0] = vertex
                    else:
                        index = 0
                        distance = float('inf')
                        for i in range(len(sweepline)):
                            current_distance = ((sweepline[i][1][0].point.x - sweepline[i][1][1].point.x) / (
                                    sweepline[i][1][0].point.y - sweepline[i][1][1].point.y) *
                                                (vertex.point.y - sweepline[i][1][1].point.y) + sweepline[i][1][
                                                    1].point.x)
                            current_distance -= vertex.point.x
                            current_distance *= -1
                            type(current_distance)
                            if current_distance > 0 and current_distance < distance:
                                distance = current_distance
                                index = i
                        if classification[sweepline[index][0].point] == 'merge':
                            new_edges.append([sweepline[index][0], vertex])
                        sweepline[index][0] = vertex
            elif classification[vertex.point] == 'start':
                start = leftmost_binary_search(edges, vertex.point.y, 0, len(edges) - 1)
                for i in range(start, len(edges)):
                    if edges[i][0].point.x == vertex.point.x:
                        sweepline.append([vertex, edges[i]])
                        break
            elif classification[vertex.point] == 'end':
                for edge in sweepline:
                    if edge[1][1].point == vertex.point:
                        if classification[edge[0].point] == 'merge':
                            new_edges.append([edge[0], edge[1][1]])
                        sweepline.remove(edge)
                        break
            elif classification[vertex.point] == 'split':
                index = 0
                distance = float('inf')
                for i in range(len(sweepline)):
                    current_distance = ((sweepline[i][1][0].point.x - sweepline[i][1][1].point.x) / (
                            sweepline[i][1][0].point.y - sweepline[i][1][1].point.y) *
                                        (vertex.point.y - sweepline[i][1][1].point.y) + sweepline[i][1][1].point.x)
                    current_distance -= vertex.point.x
                    current_distance *= -1
                    type(current_distance)
                    if current_distance > 0 and current_distance < distance:
                        distance = current_distance
                        index = i
                new_edges.append([vertex, sweepline[index][0]])
                sweepline[index][0] = vertex
                start = leftmost_binary_search(edges, vertex.point.y, 0, len(edges) - 1)
                for i in range(start, len(edges)):
                    if edges[i][0].point.x == vertex.point.x:
                        sweepline.append([vertex, edges[i]])
                        break
            elif classification[vertex.point] == 'merge':
                for edge in sweepline:
                    if edge[1][1].point == vertex.point:
                        if classification[edge[0].point] == 'merge':
                            new_edges.append([edge[0], edge[1][1]])
                        sweepline.remove(edge)
                if len(sweepline) == 1:
                    if classification[sweepline[0][0].point] == 'merge':
                        new_edges.append([sweepline[0][0], sweepline[0][1][1]])
                    sweepline[0][0] = vertex
                else:
                    index = 0
                    distance = float('inf')
                    for i in range(len(sweepline)):
                        current_distance = ((sweepline[i][1][0].point.x - sweepline[i][1][1].point.x) / (
                                sweepline[i][1][0].point.y - sweepline[i][1][1].point.y) *
                                            (vertex.point.y - sweepline[i][1][1].point.y) + sweepline[i][1][1].point.x)
                        current_distance -= vertex.point.x
                        current_distance *= -1
                        if current_distance > 0 and current_distance < distance:
                            distance = current_distance
                            index = i
                    if classification[sweepline[index][0].point] == 'merge':
                        new_edges.append([sweepline[index][0], sweepline[index][1][1]])
                    sweepline[index][0] = vertex
        self.scenes.append(Scene(lines=[LinesCollection(self.sides),
                                        LinesCollection([Point.to_line(v[0].point, v[1].point) for v in new_edges],
                                                        color='crimson')]))
        return new_edges

    def __partition_into_monotone_subpolygons(self, edges=None):
        if edges is None:
            edges = self.prepare_for_triangulation()
        vertices = {}
        vertices_index = {}
        for v in self.vertices:
            vertices[v] = []
        for i in range(len(self.vertices)):
            vertices_index[self.vertices[i]] = i
        for v1, v2 in edges:
            if vertices_index[v1] < vertices_index[v2]:
                vertices[v2].append(v1)
            else:
                vertices[v1].append(v2)
        for v in self.vertices:
            if vertices[v]:
                vertices[v].sort(key=lambda v: vertices_index[v])
        ver = self.vertices.copy()
        e = len(edges)
        subpolygons = []

        def new_subpolygon(t, index, ver, vertices, subpolygons, e):
            i = index
            j = index
            first_loop = True
            while first_loop or (e > 0 and ver[j] != t):
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
            if e == 0:
                current_subpolygon_vertices = [] + ver
            else:
                current_subpolygon_vertices = ver[i:j + 1]
            subpolygons.append(Polygon(current_subpolygon_vertices))
            return e - 1, ver[:i + 1] + ver[j:]

        new_subpolygon(ver[0], 0, ver, vertices, subpolygons, e)
        sd = []
        for sp in subpolygons:
            sd = [] + sd + sp.sides.copy()
            sp.parent = self
            self.scenes.append(Scene(lines=[LinesCollection(sp.sides.copy(), color='green')]))
            trl = []
            for tr in sp.triangles:
                trl += tr.to_list()
            self.scenes.append(Scene(lines=[LinesCollection(trl, color='crimson')]))
        return subpolygons

    def triangulate(self):
        if not self.__is_y_monotone():
            raise Exception("Triangulation error.")
            return
        if self.__is_triangulated:
            return
        if len(self.vertices) < 3:
            return
        V = sorted([[self.vertices[i], self.chain[i]] for i in range(len(self.vertices))], key=lambda v: v[0].point.y)
        if len(V) == 3:
            self.add_triangle(Triangle(V[0][0], V[1][0], V[2][0]))
            return

        def belongs(i_p, i_q, i_r) -> bool:
            p, q, r = V[i_p][0].point, V[i_q][0].point, V[i_r][0].point

            if V[i_r][1] == 1:
                return Point.orientation(p, q, r) > 0
            else:
                return Point.orientation(p, q, r) < 0

        stack = [0, 1]
        n = len(V)

        for i in range(2, n):
            if V[i][1] == V[stack[-1]][1] or V[i][1] == 0 or V[stack[-1]][1] == 0:
                new_stack = []
                while len(stack) > 1:
                    if belongs(stack[-2], stack[-1], i):
                        self.add_triangle(Triangle(V[i][0], V[stack[-1]][0], V[stack[-2]][0]))
                        stack.pop()
                    else:
                        new_stack.append(stack.pop())
                new_stack.append(stack.pop())
                new_stack.reverse()
                new_stack.append(i)
                stack = new_stack
            else:
                l = len(stack)
                ve = stack[-1]
                for j in range(l - 1):
                    self.add_triangle(Triangle(V[i][0], V[stack[-1]][0], V[stack[-2]][0]))
                    stack.pop()  # v
                stack = [ve, i]
        self.scenes.append(Scene(
            lines=[LinesCollection([tr.to_list()[i] for tr in self.triangles for i in range(3)], color='crimson')]))
        self.__is_triangulated = True

    def __triangulation(self, diagonals=None):
        if self.__is_triangulated:
            return
        if self.__is_y_monotone() and diagonals == None:
            self.triangulate()
        else:
            subpolygons = self.__partition_into_monotone_subpolygons(edges=diagonals)
            for sb in subpolygons:
                sb.__triangulation()
                self.sub_polygons.append(sb)
                if diagonals is not None:
                    for tr in list(sb.triangles):
                        self.add_triangle(tr, change=False)
                else:
                    for tr in list(sb.triangles):
                        self.add_triangle(tr)
            self.scenes += sb.scenes
        s = []
        for tr in list(self.triangles):
            s += tr.to_list()
        self.scenes.append(Scene(lines=[LinesCollection(self.sides), LinesCollection(s, color='yellow')]))
        self.__is_triangulated = True

    def actions(self, diagonals=None):
        self.__classify_vertices()
        if diagonals is not None:
            self.additional_diagonals = diagonals
        self.__triangulation(diagonals=diagonals)

    def to_scene(self, triangles=True, color='dodgerblue', color2='dodgerblue'):
        if not triangles:
            return Scene(lines=[LinesCollection(self.sides, color=color)])
        triangles = []
        for tr in self.triangles:
            triangles += tr.to_list()
        return Scene(lines=[LinesCollection(triangles, color=color2), LinesCollection(self.sides, color=color)])
