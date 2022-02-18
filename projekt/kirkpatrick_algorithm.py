from projekt import *
from projekt.GUI import LinesCollection, PointsCollection
from projekt.convex_hull import *
from projekt.GUI import *
from projekt.side import Side
from polygon import border_triangle_vertices_coords




def partition_triangle_into_polygons(tr_coord, vertices):
    point = {'bottom_left': Point(tr_coord[0][0], tr_coord[0][1]),
             'bottom_right': Point(tr_coord[2][0], tr_coord[2][1]),
             'top': Point(tr_coord[1][0], tr_coord[1][1])
             }
    polygons = {'left': [],
                'bottom': []
                }
    v_copy = vertices.copy()

    # LEFT
    max_l = 0
    max_r = 0

    for i in range(len(v_copy)):
        cur = v_copy[i]
        if Point.orientation(v_copy[max_r].point, point['bottom_left'], cur.point) == -1:
            max_r = i
        if Point.orientation(v_copy[max_l].point, point['top'], cur.point) == 1:
            max_l = i

    if max_l > max_r:
        polygons['left'] = v_copy[max_l:] + v_copy[:max_r + 1]
        v_copy = v_copy[max_r:max_l + 1]
        max_r = 0
    elif max_l < max_r:
        polygons['left'] = v_copy[max_l:max_r + 1]
        v_copy = v_copy[max_r:] + v_copy[:max_l + 1]
        max_r = max_l + 1
    else:
        polygons['left'] = v_copy
        v_copy = [v_copy[max_r]]

    # BOTTOM
    max_l = max_r
    max_r = 0

    for i in range(len(v_copy)):
        cur = v_copy[i]
        if Point.orientation(v_copy[max_r].point, point['bottom_right'], cur.point) == -1:
            max_r = i

    if max_l < max_r:
        polygons['bottom'] = v_copy[max_l:max_r + 1]
        v_copy = v_copy[:max_l] + v_copy[max_r:]
    elif max_l > max_r:
        polygons['bottom'] = v_copy[max_l:] + v_copy[:max_r + 1]
        v_copy = v_copy[max_l:max_r + 1]
    else:
        polygons['bottom'] = v_copy
        v_copy = [v_copy[max_r]]

    # RIGHT

    polygons['right'] = v_copy

    polygons['left'].reverse()
    polygons['left'] = [Vertex(point['bottom_left'])] + polygons['left'] + [Vertex(point['top'])]

    polygons['right'].reverse()
    polygons['right'] = [Vertex(point['bottom_right'])] + [Vertex(point['top'])] + polygons['right']

    polygons['bottom'].reverse()
    polygons['bottom'] = [Vertex(point['bottom_left'])] + [Vertex(point['bottom_right'])] + polygons['bottom']

    p = {'left': Polygon(polygons['left']),
         'right': Polygon(polygons['right']),
         'bottom': Polygon(polygons['bottom'])
         }

    return p


def Kirkpatrick(polygon, points, diagonals=None):
    #
    # Zebranie danych z funkcji pomocniczych
    #

    # Wizualizacja, sceny.
    kirkpatrick_scenes = []



    if not diagonals:
        diagonals = None
        polygon.sub_polygons += [polygon]

    border_triangle = Triangle(Vertex(Point(border_triangle_vertices_coords[0][0], border_triangle_vertices_coords[0][1])),
                                          Vertex(Point(border_triangle_vertices_coords[1][0], border_triangle_vertices_coords[1][1])),
                                          Vertex(Point(border_triangle_vertices_coords[2][0], border_triangle_vertices_coords[2][1])))


    tp = partition_triangle_into_polygons(border_triangle_vertices_coords, polygon.vertices)
    left = tp['left']
    right = tp['right']
    bottom = tp['bottom']
    left.actions()
    right.actions()
    bottom.actions()
    polygon.actions(diagonals=diagonals)
    polygons = [left, right, bottom, polygon]
    classfification_scene = polygon.classification_scene


    #
    # Funkcje pomocnicze:
    #

    # Zbiór wierzchołków niezależnych o maksymalnym stopniu 8
    def get_independent_set(v):
        vertices = set(v)
        n = len(vertices) // 18
        vertices_copy = list(vertices.copy())
        marked = {}
        independent_set = []
        for vertex in vertices_copy:
            marked[vertex] = False
        for vertex in border_triangle.vertices:
            marked[vertex] = True
        for vertex in vertices_copy:
            if vertex.get_degree() > 8:
                marked[vertex] = True
        for vertex in vertices_copy:
            if not marked[vertex]:
                independent_set.append(vertex)
                marked[vertex] = True
                for side in list(vertex.sides):
                    another = side.get_another_vertice(vertex)
                    if another in marked:
                        marked[another] = True
        return independent_set

    # Usuwa zadany wierzcholek, zwraca wnęke jako obiekt klasy Polygon()
    def delete_vertex(to_del_vertex: Vertex, vertices):
        polygon_vertices = []
        for side in list(to_del_vertex.sides):
            another = side.get_another_vertice(to_del_vertex)
            another.sides.remove(Side(to_del_vertex, another))
            if another in vertices + list(border_triangle.vertices):
                polygon_vertices.append(side.get_another_vertice(to_del_vertex))

        def m_ctg(vertice):
            if vertice.point.y == to_del_vertex.point.y:
                if vertice.point.x > to_del_vertex.point.x:
                    return (-1) * float('inf')
                else:
                    return float('inf')
            return (-1) * (vertice.point.x - to_del_vertex.point.x) / (
                    vertice.point.y - to_del_vertex.point.y)

        polygon_vertices.sort(key=lambda v: (-1, m_ctg(v)) if v.point.y >= to_del_vertex.point.y else (1, m_ctg(v)))
        vertices.remove(to_del_vertex)
        return Polygon(polygon_vertices)

    # Sprawdzamy czy trojkaty na siebie nachodza.
    # Analizujemy każdą możliwą parę rodzic - dziecko,
    # ponieważ takich par jest zawsze maksymalnie 8 * (8-6),
    # ze względu na wybierane wierzcholki o stopniu maksymalnym rownym 8.
    # Powstalych wnęk jest n/18, dla każdej funkcja update_triangles
    # wykonuje maksymalnie 48 operacji, zatem metoda ta ma zlożonośc O(n).
    def update_triangles(parents, children):
        for child in list(children):
            for v in list(child.vertices):
                v.remove_triangle(child)
        for parent in list(parents):
            for child in list(children):
                if Triangle.do_overlap(parent, child):
                    parent.add_child(child)

    vertices = polygon.vertices.copy()
    triangle_polygons = partition_triangle_into_polygons(border_triangle_vertices_coords,
                                                         vertices)
    for k in triangle_polygons.keys():
        triangle_polygons[k].actions()
    kirkpatrick_scenes.append(Scene(
        points=[PointsCollection([v.point.to_tuple() for v in vertices])],
        lines=[LinesCollection([s for v in vertices for vt in v.triangles for s in vt.to_list()], color='lightsteelblue')] + \
              [LinesCollection(
                  [[border_triangle_vertices_coords[i % 3], border_triangle_vertices_coords[(i + 1) % 3]] for i in range(3)],
                  color='navy')] + \
              # [LinesCollection([s for s in border_triangle.to_list()], color='navy')] + \
              [LinesCollection([s for ptr in polygons[-1].triangles for s in ptr.to_list()], color='mistyrose')] + \
              [LinesCollection([s for s in polygon.sides], color='red')] + \
              [LinesCollection([[v[0].point.to_tuple(), v[1].point.to_tuple()] for v in polygon.additional_diagonals],
                               color='red')]
    ))
    deleted_set_scenes = []
    polygons_set_triang_scenes = dict()
    while len(vertices) > 1:
        polygons = []
        S = get_independent_set(vertices)
        deleted_set_scenes.append(Scene(
            lines=[LinesCollection([s for v in vertices.copy() for tr in v.triangles.copy() for s in tr.to_list()],
                                   color='lightsteelblue')]
        ))
        for vertex in S:
            # before deletion scene
            kirkpatrick_scenes.append(Scene(
                points=[PointsCollection([v.point.to_tuple() for v in vertices])] + \
                       [PointsCollection([vertex.point.to_tuple()], color='red')],
                lines=[LinesCollection([s for v in vertices for vt in v.triangles for s in vt.to_list()],
                                       color='lightsteelblue')] + \
                      [LinesCollection([s for s in border_triangle.to_list()], color='navy')] + \
                      [LinesCollection([s for ctr in vertex.triangles for s in ctr.to_list()], color='orangered')]
            ))
            if len(vertices) == 1:
                break
            polygons.append(delete_vertex(vertex, vertices))
            polygons_set_triang_scenes[polygons[-1]] = Scene(
                lines=[LinesCollection([s for v in vertices.copy() for tr in v.triangles.copy() for s in tr.to_list()],
                                       color='lightsteelblue')]
            )
            if not polygons:
                raise Exception("Error")
                return
            polygons[-1].actions()
            # for p in polygons:
            #     polygons_set_triang_scenes[p] = Scene(
            #         lines=[LinesCollection([s for v in vertices for vt in v.triangles for s in vt.to_list()],
            #                                color='lightsteelblue')] + \
            #               [LinesCollection([s for s in border_triangle.to_list()], color='navy')] + \
            #               [LinesCollection([s for ptr in polygons[-1].triangles for s in ptr.to_list()], color='darkgreen')]
            #     )
            update_triangles(polygons[-1].triangles.copy(), vertex.triangles.copy())
            # polygons_set_triang_scenes[polygons[-1]] = Scene(
            #             lines=[LinesCollection([s for v in vertices for vt in v.triangles for s in vt.to_list()],
            #                                    color='lightsteelblue')] #+ \
            #                  # [LinesCollection([s for s in border_triangle.to_list()], color='navy')] + \
            #                   #[LinesCollection([s for ptr in polygons[-1].triangles for s in ptr.to_list()], color='darkgreen')]
            #         )

            # after deletion scene
            kirkpatrick_scenes.append(Scene(
                points=[PointsCollection([v.point.to_tuple() for v in vertices])],
                lines=[LinesCollection([s for v in vertices for vt in v.triangles for s in vt.to_list()],
                                       color='lightsteelblue')] + \
                      [LinesCollection([s for s in border_triangle.to_list()], color='navy')] + \
                      [LinesCollection([s for ptr in polygons[-1].triangles for s in ptr.to_list()], color='darkgreen')]
            ))
            if len(vertices) == 1:
                for vtr in vertices[0].triangles:
                    border_triangle.add_child(vtr)
                    polygons_set_triang_scenes[polygons[-1]] = Scene(
                        lines=[LinesCollection([s for v in vertices.copy() for tr in v.triangles.copy() for s in tr.to_list()],
                                               color='lightsteelblue')]
                    )
    border_triangle.polygon = polygons[-1]
    deleted_set_scenes.append(Scene(
        lines=[LinesCollection([s for v in vertices.copy() for tr in v.triangles.copy() for s in tr.to_list()],
                               color='lightsteelblue')]
    ))


    def locate_point(p: Point):
        locate_point_scenes = []
        root = border_triangle
        selected = None
        i = len(deleted_set_scenes) - 1
        while root.children:
            s_lines = polygons_set_triang_scenes[selected.polygon if selected is not None else root.polygon].lines
            locate_point_scenes.append(Scene(
                lines=s_lines + \
                      [LinesCollection([s for child in root.children for s in child.to_list()])] + \
                      [LinesCollection([s for s in border_triangle.to_list()], color='navy')],
                points=[PointsCollection([p.to_tuple()], color='orange')]
            ))

            for child in root.children:
                locate_point_scenes.append(Scene(
                    lines=s_lines  + \
                          [LinesCollection([s for rchild in root.children for s in rchild.to_list()])] + \
                          [LinesCollection([s for s in border_triangle.to_list()], color='navy')] + \
                          [LinesCollection([s for s in child.to_list()], color='gold')],
                    points=[PointsCollection([p.to_tuple()], color='orange')]
                ))
                if child.is_in_triangle(p):
                    selected = child
                    break

            locate_point_scenes.append(Scene(
                lines=s_lines + \
                      [LinesCollection([s for child in root.children for s in child.to_list()])] + \
                      [LinesCollection([s for s in border_triangle.to_list()], color='navy')] + \
                      [LinesCollection([s for s in selected.to_list()], color='forestgreen')],
                points=[PointsCollection([p.to_tuple()], color='orange')]
            ))
            if selected == root:
                break
            root = selected
            i -= 1
        if root.polygon in polygon.sub_polygons:
            locate_point_scenes.append(Scene(
                lines=deleted_set_scenes[0].lines + \
                      root.polygon.to_scene(triangles=False).lines + \
                      [LinesCollection([s for s in border_triangle.to_list()], color='navy')] + \
                      [LinesCollection([s for s in root.to_list()], color='forestgreen')],
                points=[PointsCollection([p.to_tuple()], color='green')]
            ))
            locate_point_scenes.append(Scene(
                lines=deleted_set_scenes[0].lines + \
                      polygon.to_scene(triangles=False).lines + \
                      [LinesCollection([s for s in border_triangle.to_list()], color='navy')] + \
                      [LinesCollection(
                          [[v[0].point.to_tuple(), v[1].point.to_tuple()] for v in polygon.additional_diagonals],
                          color='lightsteelblue')] + \
                      root.polygon.to_scene(triangles=False, color='green').lines,
                points=[PointsCollection([p.to_tuple()], color='green')]
            ))
        else:
            locate_point_scenes.append(Scene(
                lines=deleted_set_scenes[0].lines + \
                      polygon.to_scene(triangles=False).lines + \
                      [LinesCollection([s for s in border_triangle.to_list()], color='navy')] + \
                      [LinesCollection(
                          [[v[0].point.to_tuple(), v[1].point.to_tuple()] for v in polygon.additional_diagonals],
                          color='lightsteelblue')] + \
                      [LinesCollection([s for s in root.to_list()], color='lightcoral')],
                points=[PointsCollection([p.to_tuple()], color='red')]
            ))

        return locate_point_scenes

    loc_scenes = []
    for p in points:
        loc_scenes += locate_point(p)
    return [classfification_scene] + kirkpatrick_scenes + loc_scenes
