from graph import *

# node1 = Node(10,5)
# node2 = Node(12,1)
# node3 = Node(3,4)
# node4 = Node(4,9)
# node1.setNeighbors({node2, node3, node4})
# node2.setNeighbors({node1,node2})
# node3.setNeighbors({node1})

# graph = Graph({node1, node2, node3, node4})

def transpile(g):
    color="red!20"
    shape="circle"
    size="1cm"
    def getNodeString(node):
      return "({0},{1}) node[{2}, fill={3}, minimum size={4}] {5};\n".format(node.x_pos, node.y_pos, shape, color, size, "{}")
    def getEdgeString(node1, node2):
      return "({0},{1}) -- ({2},{3});\n".format(node1.x_pos, node1.y_pos, node2.x_pos, node2.y_pos)

    f = open("output.tex", 'w')
    f.write("\documentclass{article}\n\usepackage{tikz}\n\\begin{document}\n\\begin{tikzpicture}\n")
    for node in g.nodes:
      for neighbor in node.neighbors:
        f.write("\t\\draw " + getEdgeString(node, neighbor))
    for node in g.nodes:
      f.write("\t\\draw " + getNodeString(node))   
    f.write("\end{tikzpicture}\n\end{document}")

