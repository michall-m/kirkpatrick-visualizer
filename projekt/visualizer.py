from projekt.kirkpatrick_algorithm import *
from projekt.draw_polygon import *


class Visualizer:
    def __init__(self, filename):
        self.filename = filename
        self.visualization = DrawPolygon(filename)

    def run(self):
        if not self.visualization.exists:
            self.visualization.draw(init_config=True)
            self.visualization.save_changes()
        self.visualization.generate_data()
        self.visualization.plot = Plot(Kirkpatrick(self.visualization.main_polygon, self.visualization.points, diagonals=self.visualization.diagonals))
        self.visualization.plot.draw()