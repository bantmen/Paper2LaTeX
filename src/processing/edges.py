import numpy as np
from Queue import Queue
from itertools import repeat, chain, product

from graph.graph import Graph, Node


PIXEL_UNVISITED = 0 # Value of an unvisited pixel.
PIXEL_VISITED = 1 # Value of a visited pixel.
PIXEL_BG = 255 # Value of a background pixel.

def find_edges(image, nodes, bbox_edges):
    """ Finds the edges between nodes in the given image.

    image -- a 2d Numpy ndarray
    nodes -- a list of the nodes detected in the image
    bbox_edges -- a dictionary indicating whether a pixel at a given coordinate is on the edge of a node's bounding box
    """

    # Dictionary mapping each node to its immediate neighbourhood.
    nbhds = {}

    for node in nodes:
        nbhds[node] = find_nbhd(image, nodes, bbox_edges, node)

    return make_graph(nbhds)

def find_nbhd(image, nodes, bbox_edges, node):
    """ Finds all of the nodes that are adjacent to the given node in the image.

    image -- a 2d Numpy ndarray
    nodes -- a list of the nodes detected in the image
    bbox_edges -- a dictionary indicating whether a pixel at a given coordinate is on the edge of a node's bounding box
    node -- the node whose edges we wish to find
    """
    #start = node.rep_pixel # Some representative pixel that is a black pixel on the node.
    nbhd = set()

    # Find clusters of unvisited pixels along the border of the bounding box;
    # these will be the starting points for traversing the pixels in each edge.
    out_srcs = find_unvisited_out_srcs(image, node)

    for pixel in out_srcs:
        nbhd = nbhd.union(traverse_edge(image, nodes, bbox_edges, node, start_pixel))

    return nbhd

def find_unvisited_out_srcs(image, node):
    """ Returns a set of pixel representatives of unvisited edges incident to the given node. """
    bbox_tl = node.bbox_tl
    bbox_br = node.bbox_br

    bbox_tr = (bbox_br[0], bbox_tl[1])
    bbox_bl = (bbox_tl[0], bbox_br[1])

    #bbox_width = abs(bbox_br[0] - bbox_tl[0])
    #bbox_height = abs(bbox_br[1] - bbox_tl[1])

    # Generate a list of all pixels on the bounding box.
    tl_to_tr = zip(range(bbox_tl[0], bbox_tr[0]), repeat(bbox_tl[1])) # Top left to top right.
    tr_to_br = zip(repeat(bbox_tr[0]), range(bbox_tr[1], bbox_br[1])) # Top right to bottom right.
    br_to_bl = zip(range(bbox_br[0], bbox_bl[0], -1), repeat(bbox_br[1])) # Bottom right to bottom left.
    bl_to_tl = zip(repeat(bbox_bl[0]), range(bbox_bl[1], bbox_tl[1], -1)) # Bottom left to top left.

    bbox_iter = chain(tl_to_tr, tr_to_br, br_to_bl, bl_to_tl)

    reps = []
    cur_rep = None
    for pixel in bbox_iter:
        if image[pixel] == PIXEL_UNVISITED:
            if not cur_rep:
                cur_rep = pixel
                reps.append(pixel)
        else:
            cur_rep = None

    return reps

def traverse_edge(image, nodes, bbox_edges, node, start_pixel):
    frontier = Queue()
    frontier.put(start_pixel)

    found_nodes = set()

    while not frontier.empty():
        current = frontier.get()
        image[current] = PIXEL_VISITED
        if current in bbox_edges:
            found_nodes.add(bbox_edges[current])
            continue # Don't expand current pixel if it is on the boundary of a bounding box.

        for pixel in adjacent_pixels(current, image.shape):
            if pixel == PIXEL_UNVISITED:
                frontier.put(pixel)

    return found_nodes

def adjacent_pixels(pixel, image_shape):
    adjacent = []
    directions = product([-1, 0, 1], [-1, 0, 1])
    for dr in directions:
        if dr == (0, 0):
            continue

        adj = (pixel[0] + dr[0], pixel[1] + dr[1])
        if adj[0] >= 0 and adj[1] >= 0 and adj[0] < image_shape[0] and adj[1] < image_shape[1]:
            adjacent.append(adj)

    return adjacent

def make_graph(nbhds):
    """ Generates a Graph object from the dictionary of neighborhoods. """
    nodes = set()
    for node in nbhds.keys():
        nodes.add(Node(node.center[0], node.center[1], nbhds[node]))

    return Graph(nodes)

class ImageNode():
    def __init__(self, bbox_tl, bbox_br, center):
        self.bbox_tl = bbox_tl
        self.bbox_br = bbox_br
        self.center = center

    def __hash__(self):
        return center.__hash__()

"""
if __name__ == "__main__":
    a = np.ndarray(shape=(4, 4), buffer=np.array([[0, 0, 255, 255], [0, 255, 255, 255], [255, 255, 255, 0], [255, 0, 0, 255]]))
    print a
    find_unvisited_out_srcs(a, ImageNode((0, 0), (3, 3)))

    print
    print
    adjacent_pixels((0, 3), (5, 5))
"""

