from projekt import *
from projekt.ConvexHull import *
from projekt.main import *

def ch_triangle(ch_vertices, delta = 1):
    first_p = ch_vertices[0].point
    min_y = first_p.y
    max_y = first_p.y
    min_x = first_p.x
    max_x = first_p.x

    for v in ch_vertices:
        min_y = min(min_y, v.point.y)
        max_y = max(max_y, v.point.y)
        min_x = min(min_x, v.point.x)
        max_x = max(max_x, v.point.x)

    a = max(max_y-min_y, max_x - min_x)
    tr = [(min_x - a/2.0 - delta, min_y - delta/2.0), (min_x + a/2.0, min_y + 2.0 * a + delta), (min_x + 3.0*a/2.0 + delta, min_y - delta/2.0)]
    triangle = Triangle(Vertex(Point(tr[0][0], tr[0][1])),
                        Vertex(Point(tr[1][0], tr[1][1])),
                        Vertex(Point(tr[2][0], tr[2][1])))
    tr_center = Point((tr[0][0] + tr[2][0]) / 2.0, (tr[0][1] + tr[1][1]) / 2.0)
    t = {'triangle': triangle,
         'tr_coord': tr,
         'tr_center': tr_center
         }
    return t

def failed_partition_triangle_into_polygons(triangle, tr_center, tr_coord, ch_vertices, vertices):
    point = {'bottom_left': Point(tr_coord[0][0], tr_coord[0][1]),
             'bottom_right': Point(tr_coord[2][0], tr_coord[2][1]),
             'top': Point(tr_coord[1][0], tr_coord[1][1])
             }
    polygons = {'left': [], #TODO dodaj vertexy trojkata i zastanow się nad posortowaniem wierzcholkow
                'right': [],
                'bottom': []
                }
    vertices_no = []
    for v in ch_vertices:
        bottom_left_orientation = Point.orientation(point['bottom_left'], tr_center, v.point)
        bottom_right_orientation = Point.orientation(point['bottom_right'], tr_center, v.point)
        top_orientation = Point.orientation(point['top'], tr_center, v.point)

        if bottom_left_orientation == 1 and bottom_right_orientation == -1:
            #polygons['bottom'].append(v)
            vertices_no.append('bottom')
            continue
        if bottom_right_orientation == 1 and top_orientation == -1:
            #polygons['right'].append(v)
            vertices_no.append('right')
            continue
        if top_orientation == 1 and bottom_left_orientation == -1:
            #polygons['left'].append(v)
            vertices_no.append('left')
            continue
        print("error in for v in ch_vertices in partition_triangle_into_polygons in Kirkpatrick")
    """
    most_left = min(ch_vertices, key = lambda v: (v.point.y, v.point.x))
    def f(b,c):
        #if not polygons['left']:
        #    return 1
        #v_s = Vertex(Point((tr_coord[0][0] + tr_coord[1][0]) / 2.0, (tr_coord[0][1] + tr_coord[1][1]) / 2.0))
        #v_s = polygons['left'][-1]
        return comparing_f(most_left, b, c)
    def g(b,c):
        if not polygons['bottom']:
            return 1
        #v_s = Vertex(Point((tr_coord[0][0] + tr_coord[2][0]) / 2.0, (tr_coord[0][1] + tr_coord[2][1]) / 2.0))
        v_s = polygons['bottom'][-1]
        return comparing_f(v_s, b, c)
    def h(b,c):
        if not polygons['right']:
            return 1
        #v_s = Vertex(Point((tr_coord[1][0] + tr_coord[2][0]) / 2.0, (tr_coord[1][1] + tr_coord[2][1]) / 2.0))
        v_s = polygons['right'][-1]
        return comparing_f(v_s, b, c)
    """

    i = 0
    j = 0
    while(i < len(ch_vertices)):
        while j < len(ch_vertices) and vertices_no[i] == vertices_no[j]:
            j += 1
        polygons[vertices_no[i]] = ch_vertices[i:j] + polygons[vertices_no[i]]
        i = j

    if polygons['left']:
        polygons['right'] += [polygons['left'][0]]
        polygons['bottom'] += [polygons['right'][0]]
        polygons['left'] += [polygons['bottom'][0]]
    elif polygons['right']:
        polygons['bottom'] += [polygons['right'][0]]
        polygons['left'] += [polygons['bottom'][0]]
        polygons['right'] += [polygons['left'][0]]
    elif polygons['bottom']:
        polygons['left'] += [polygons['bottom'][0]]
        polygons['right'] += [polygons['left'][0]]
        polygons['bottom'] += [polygons['right'][0]]



    for k in list(polygons.keys()):
        if not polygons[k]:
            continue
        i = 0
        while i < len(vertices) and vertices[i] != polygons[k][0]:
            i += 1
        j = i
        while vertices[j%len(vertices)] != polygons[k][-1]:
            j += 1
        j = j%len(vertices)
        if i <= j:
            polygons[k] = vertices[i:j+1]
        elif j < i:
            polygons[k] = vertices[i:] + vertices[:j+1]




    #polygons['left'].sort(key = cmp_to_key(f))
    #polygons['right'].sort(key=cmp_to_key(h))
    #polygons['bottom'].sort(key = cmp_to_key(g))
    polygons['left'].reverse()
    polygons['left'] = [Vertex(point['bottom_left'])] + polygons['left'] + [Vertex(point['top'])]

    polygons['right'].reverse()
    polygons['right'] = [Vertex(point['bottom_right'])] + [Vertex(point['top'])] + polygons['right']

    polygons['bottom'].reverse()
    polygons['bottom'] = [Vertex(point['bottom_left'])] + [Vertex(point['bottom_right'])] + polygons['bottom']
    """
    for k in list(polygons.keys()):
        v_min = min(polygons[k], key = lambda v: (v.point.y, v.point.x))
        def func(b,c):
            return comparing_f(v_min, b, c)
        polygons[k].sort(key = cmp_to_key(func))
    """

    p = {'left': Polygon(polygons['left']),
         'right': Polygon(polygons['right']),
         'bottom': Polygon(polygons['bottom'])
         }

    return p

def partition_triangle_into_polygons(triangle, tr_center, tr_coord, ch_vertices, vertices):
    point = {'bottom_left': Point(tr_coord[0][0], tr_coord[0][1]),
             'bottom_right': Point(tr_coord[2][0], tr_coord[2][1]),
             'top': Point(tr_coord[1][0], tr_coord[1][1])
             }
    polygons = {'left': [], #TODO dodaj vertexy trojkata i zastanow się nad posortowaniem wierzcholkow
                'right': [],
                'bottom': []
                }
    v_copy = vertices.copy()

    #LEFT
    max_l = 0
    max_r = 0

    for i in range(len(v_copy)):
        cur = v_copy[i]
        if Point.orientation(v_copy[max_r].point, point['bottom_left'], cur.point) == -1:
            max_r = i
        if Point.orientation(v_copy[max_l].point, point['top'], cur.point) == 1:
            max_l = i

    if max_l > max_r:
        polygons['left'] = v_copy[max_l:] + v_copy[:max_r+1]
        v_copy = v_copy[max_r:max_l+1]
    elif max_l < max_r:
        polygons['left'] = v_copy[max_l:max_r+1]
        v_copy = v_copy[max_l:] + v_copy[:max_r+1]
    else:
        polygons['left'] = v_copy
        v_copy = [v_copy[max_r]]

    #BOTTOM
    max_l = 0
    max_r = 0

    for i in range(len(v_copy)):
        cur = v_copy[i]
        if Point.orientation(v_copy[max_l].point, point['bottom_left'], cur.point) == 1:
            max_l = i
        if Point.orientation(v_copy[max_r].point, point['bottom_right'], cur.point) == -1:
            max_r = i

    if max_l < max_r:
        polygons['bottom'] = v_copy[max_l:max_r+1]
        v_copy = v_copy[:max_l+1] + v_copy[max_r:]
    elif max_l > max_r:
        polygons['bottom'] = v_copy[max_l:] + v_copy[:max_r+1]
        v_copy = v_copy[max_l:max_r+1]
    else:
        polygons['bottom'] = v_copy
        v_copy = [v_copy[max_r]]

    #RIGHT

    polygons['right'] = v_copy

    polygons['left'].reverse()
    polygons['left'] = [Vertex(point['bottom_left'])] + polygons['left'] + [Vertex(point['top'])]

    polygons['right'].reverse()
    polygons['right'] = [Vertex(point['bottom_right'])] + [Vertex(point['top'])] + polygons['right']

    polygons['bottom'].reverse()
    polygons['bottom'] = [Vertex(point['bottom_left'])] + [Vertex(point['bottom_right'])] + polygons['bottom']
    """
    for k in list(polygons.keys()):
        v_min = min(polygons[k], key = lambda v: (v.point.y, v.point.x))
        def func(b,c):
            return comparing_f(v_min, b, c)
        polygons[k].sort(key = cmp_to_key(func))
    """

    p = {'left': Polygon(polygons['left']),
         'right': Polygon(polygons['right']),
         'bottom': Polygon(polygons['bottom'])
         }

    return p

def Kirkpatricick(polygon):
    #
    # Zebranie danych z funkcji pomocniczych
    #
    gs = graham_scan(polygon.vertices)
    bt = ch_triangle(gs) #biggest triangle
    tp = partition_triangle_into_polygons(bt['triangle'], bt['tr_center'], bt['tr_coord'], gs, polygon.vertices)
    left = tp['left']
    right = tp['right']
    bottom = tp['bottom']
    left.actions()
    right.actions()
    bottom.actions()
    polygon.actions()
    #test_partition_triangle_into_polygons(bt['triangle'], bt['tr_center'], bt['tr_coord'], gs, polygon.vertices)

    polygons = [left, right, bottom, polygon]

    #
    # Wizualizacja, sceny
    #
    kirkpatrick_scenes = []
    triangles_vizu = {'left':[],
                      'right':[],
                      'bottom':[],
                      'polygon':[]
                      }

    for tr in left.triangles:
        triangles_vizu['left'] += tr.to_list()
    for tr in right.triangles:
        triangles_vizu['right'] += tr.to_list()
    for tr in bottom.triangles:
        triangles_vizu['bottom'] += tr.to_list()
    for tr in polygon.triangles:
        triangles_vizu['polygon'] += tr.to_list()

    kirkpatrick_scenes.append(Scene(lines = [LinesCollection(triangles_vizu['left'], color = 'yellow'),
                                      LinesCollection(triangles_vizu['right'], color = 'green'),
                                      LinesCollection(triangles_vizu['bottom'], color = 'blue'),
                                      LinesCollection(triangles_vizu['polygon'], color = 'crimson')
                                      ]))

    #def add_kirkpatrick_scene(P, l, r, b): #polygons list, left, right, bottom



    #
    # Funkcje pomocnicze:
    #

    # Zbiór wierzchołków niezależnych o maksymalnym stopniu 8
    def get_independent_set(v):
        vertices = set(v)
        n = len(vertices)//18
        vertices_copy = list(vertices.copy())
        marked = {}
        independent_set = []
        for vertex in vertices_copy:
            marked[vertex] = False
        for vertex in bt['triangle'].vertices:
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
            if another in vertices:
                polygon_vertices.append(side.get_another_vertice(to_del_vertex))
        def f(b,c):
            return comparing_f(to_del_vertex, b, c)
        polygon_vertices.sort(key = cmp_to_key(f))
        vertices.remove(to_del_vertex)
        return Polygon(polygon_vertices)



    #
    # Główna pętla:
    #

    vertices = polygon.vertices.copy()
    while len(vertices) > 12:
        polygons = []
        S = get_independent_set(vertices)
        for vertex in S:
            if len(vertices) == 12:
                break
            polygons.append(delete_vertex(vertex, vertices))
            if not polygons:
                print("not polygons")
                return
            polygons[-1].actions()
            convex_hull_vertices = graham_scan(vertices)
            bt = ch_triangle(convex_hull_vertices)
            triangle_polygons = partition_triangle_into_polygons(bt['triangle'],
                                                                 bt['tr_center'],
                                                                 bt['tr_coord'],
                                                                 convex_hull_vertices,
                                                                 vertices)
            for k in triangle_polygons.keys():
                kirkpatrick_scenes.append(triangle_polygons[k].to_scene())
                triangle_polygons[k].actions()
                kirkpatrick_scenes += triangle_polygons[k].scenes
            current_lines = []
            for pol in polygons:
                current_lines += pol.to_scene().lines
            current_lines += triangle_polygons['left'].to_scene(color='yellow').lines + \
                triangle_polygons['right'].to_scene(color = 'green').lines + \
                triangle_polygons['bottom'].to_scene(color='blue').lines + \
                [LinesCollection([[convex_hull_vertices[ii].point.to_tuple(),
                                   convex_hull_vertices[(ii+1)%len(convex_hull_vertices)].point.to_tuple()]
                                  for ii in range(len(convex_hull_vertices))],
                                 color = 'red')]
            kirkpatrick_scenes.append(Scene(lines = current_lines))




    #ppppp = delete_vertex(S[0], vertices)
    #ppppp.actions()
    plot = Plot(kirkpatrick_scenes)
    #plot.add_scene(Scene(lines=ppppp.to_scene(color = 'crimson').lines + left.to_scene().lines + right.to_scene().lines + bottom.to_scene().lines))
    plot.draw()