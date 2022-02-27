import sys

from visualizer import Visualizer

if __name__ == "__main__":
    if len(sys.argv) == 1:
        polygon_name = 'polygon'
    elif len(sys.argv) != 2:
        raise Exception("The only argument must be <polygon_name>.")
    else:
        polygon_name = sys.argv[1]
    visualizer = Visualizer(polygon_name)
    visualizer.run()

