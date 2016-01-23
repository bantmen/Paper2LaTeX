import numpy as np
from processing.edges import *
from processing.processing import *
from graph.compile import transpile

if __name__ == "__main__":
    # a = np.ndarray(shape=(4, 4), buffer=np.array([[0, 0, 255, 255], [0, 255, 255, 255], [255, 255, 255, 0], [255, 0, 0, 255]]))
    # print a
    # find_unvisited_out_srcs(a, ImageNode((0, 0), (3, 3), (1, 1)))

    # print
    # print
    # adjacent_pixels((0, 3), (5, 5))

    file_name = '../images/2016-01-22 14.49.05.jpg'
    img_nodes, img = get_semantics(file_name)
    bbox_edges = make_bbox_edge_dict(img_nodes)
    graph = find_edges(img, img_nodes, bbox_edges)
    print graph
    #fuck(graph)
    transpile(graph)
