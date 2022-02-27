from GUI import *
import os
from point import Point
from polygon import Polygon
from vertex import Vertex
from polygon import border_triangle_vertices_coords



class DrawPolygon:
    def __init__(self, name):
        self.segments = []
        self.name = name
        self.json_filename = self.name + '.json'
        self.plot = Plot(scenes=[Scene(
            lines=[LinesCollection(
                [[border_triangle_vertices_coords[i % 3], border_triangle_vertices_coords[(i + 1) % 3]] for i in range(3)], color='navy')])])
        self.exists = False
        self.create_json()
        self.vertices = []

        # edges intersecting the polygon
        self.diagonals = []
        self.main_polygon = None

        # point to locate
        self.points = []

    def create_json(self):
        current_path = os.path.abspath(os.getcwd()) + '/Sets' + '/' + self.json_filename
        if not os.path.exists(current_path):
            with open(current_path, 'w+'):
                return None
        else:
            with open(current_path, 'r') as json_file:
                self.plot = Plot(json=json_file.read())
            self.exists = True

    def save_changes(self):
        current_path = os.path.abspath(os.getcwd()) + '/Sets' + '/' + self.json_filename
        new_plot = Plot(scenes=[self.plot.get_added_elements()])
        with open(current_path, 'w+') as json_file:
            json_file.write(new_plot.to_json())
        self.plot = new_plot

    def draw(self, **kwargs):
        self.plot.draw(**kwargs)

    def __hash__(self):
        return hash(self.name)

    def delete(self):
        self.plot = Plot(scenes=[Scene()])
        current_path = os.path.abspath(os.getcwd()) + '/Sets' + '/' + self.json_filename
        if os.path.exists(current_path):
            with open(current_path, 'w') as json_file:
                os.remove(json_file.name)

    def generate_data(self):
        if self.main_polygon is not None:
            return

        current_path = os.path.abspath(os.getcwd()) + '/Sets' + '/' + self.json_filename
        with open(current_path, 'r') as json_file:
            json_data = js.loads(json_file.read())[0]

        def in_tolerance(v1, v2, tolerance=0.02, t_range=20):
            return np.sqrt(
                np.power(v1.point.x - v2.point.x, 2) + np.power(v1.point.y - v2.point.y, 2)) < tolerance * t_range

        self.vertices = [Vertex(Point(p[1][0], p[1][1])) for p in json_data['lines'][1]]
        self.main_polygon = Polygon(self.vertices)

        for d in json_data['lines'][0]:
            v1 = None
            v2 = None
            for v in self.vertices:
                if in_tolerance(v, Vertex(Point(d[0][0], d[0][1]))):
                    v1 = v
                elif in_tolerance(v, Vertex(Point(d[1][0], d[1][1]))):
                    v2 = v
            if v1 is None or v2 is None:
                raise Exception("Incorrect diagonal.")
            else:
                self.diagonals.append([v1, v2])
        self.points = [Point(p[0], p[1]) for p in json_data['points'][0]]
