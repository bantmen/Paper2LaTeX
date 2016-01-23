import numpy as np
from processing.edges import *

if __name__ == "__main__":
    a = np.ndarray(shape=(4, 4), buffer=np.array([[0, 0, 255, 255], [0, 255, 255, 255], [255, 255, 255, 0], [255, 0, 0, 255]]))
    print a
    find_unvisited_out_srcs(a, ImageNode((0, 0), (3, 3), (1, 1)))

    print
    print
    adjacent_pixels((0, 3), (5, 5))
