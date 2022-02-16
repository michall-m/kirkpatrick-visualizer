from projekt.Triangle import Triangle
from projekt.Point import Point
from projekt.Vertex import Vertex
from projekt.GUI import *
from projekt.Polygon import Polygon
from projekt.ConvexHull import graham_scan
from projekt.KirkpatrickAlgorithm import *
from projekt.DrawPolygon import *
from multiprocessing import Process
from time import sleep


if __name__ == "__main__":
    """
    Przykładowy wielokat niemonotoniczny:
    test_data = [[2.00289818548387, 4.782475490196079],
                 [-1.74710181451613, 9.132965686274508],
                 [-3.27935987903226, 6.559436274509805],
                 [-4.85194052419355, 8.70404411764706],
                 [-8.118069556451614, 4.0471813725490176],
                 [-4.89226310483871, -0.3645833333333339],
                 [-2.7148437500000018, 1.2285539215686274],
                 [-4.932585685483872, 3.0055147058823533],
                 [-2.513230846774194, 4.476102941176469],
                 [-1.2229082661290338, -0.303308823529413],
                 [-3.92452116935484, -3.3057598039215694],
                 [-7.110005040322582, -1.344975490196079],
                 [-8.239037298387098, -5.3278186274509824],
                 [-4.730972782258066, -8.943014705882355],
                 [-2.02935987903226, -5.6341911764705905],
                 [0.1883820564516121, -9.065563725490197],
                 [2.365801411290322, -4.776348039215687],
                 [-0.09387600806451779, -6.124387254901963]]
    """
    tdp = DrawPolygon('test15')
    if not tdp.exists:
        p = Process(target=tdp.draw())
        p.start()
        p.join()
        tdp.save_changes()
    tdp.generate_data()
    tdp.plot = Plot(Kirkpatrick(tdp.main_polygon, tdp.points, diagonals=tdp.diagonals))
    tdp.plot.draw()