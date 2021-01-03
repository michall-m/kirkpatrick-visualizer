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

def partition_triangle_into_polygons(triangle, tr_center, tr_coord, ch_vertices, vertices):
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



def Kirkpatricick(polygons):
    p = polygons[0]
    gs = graham_scan(p.vertices)
    t = ch_triangle(gs)
    tp = partition_triangle_into_polygons(t['triangle'], t['tr_center'], t['tr_coord'], gs, p.vertices)
    l = tp['left']
    r = tp['right']
    b = tp['bottom']
    l.actions()
    r.actions()
    b.actions()
    triangles_vizu = {'l':[],
                      'r':[],
                      'b':[]
                      }
    for tr in l.triangles:
        triangles_vizu['l'] += tr.to_list()
    for tr in r.triangles:
        triangles_vizu['r'] += tr.to_list()
    for tr in b.triangles:
        triangles_vizu['b'] += tr.to_list()
    return Scene(lines = [LinesCollection(triangles_vizu['l'], color = 'yellow'),
                          LinesCollection(triangles_vizu['r'], color = 'green'),
                          LinesCollection(triangles_vizu['b'], color = 'blue')
                          ]
                 )