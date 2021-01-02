from projekt import *

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
    tr_center = [(tr[0][0] + tr[2][0]) / 2.0, (tr[0][1] + tr[1][1]) / 2.0]
    return triangle, tr_center

def partition_triangle_into_polygons(triangle, tr_center, ch_vertices):
    polygons = {'left': [],
                'right': [],
                'bottom': []}



def Kirkpatricick(polygons):
    z = 134