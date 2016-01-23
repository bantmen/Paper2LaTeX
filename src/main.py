import numpy as np
import cv2

from ..processing.edges import *
from ..processing.processing import *
from ..graph.compile import transpile

if __name__ == "__main__":
    file_name = '../images/2016-01-22 20.21.52.jpg'
    img_nodes, img = get_semantics(file_name)
    bbox_edges = make_bbox_edge_dict(img_nodes)
    graph = find_edges(img, img_nodes, bbox_edges)

    cv2.imshow('asdf', img)
    #cv2.resizeWindow('asdf', 800, 600)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print graph

    width, height = img.shape
    transpile(graph, width, height)
