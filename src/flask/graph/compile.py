from graph import *

# node1 = Node(10,5)
# node2 = Node(12,1)
# node3 = Node(3,4)
# node4 = Node(4,9)
# node1.setNeighbors({node2, node3, node4})
# node2.setNeighbors({node1,node2})
# node3.setNeighbors({node1})

# graph = Graph({node1, node2, node3, node4})

def transpile(g, width, height):
    color="red!20"
    shape="circle"
    size="1cm"

    def getNodeString(node):
      return "({0},{1}) node[{2}, fill={3}, minimum size={4}] {5};\n".format(node.x/float(width)*8, 8-node.y/float(height)*8, shape, color, size, "{}")
    def getEdgeString(node1, node2):
      return "({0},{1}) -- ({2},{3});\n".format(node1.x/float(width)*8, 8-node1.y/float(height)*8, node2.x/float(width)*8, 8-node2.y/float(height)*8)

    f = open("output.tex", 'w')
    f.write("\documentclass{article}\n\usepackage{tikz}\n\\begin{document}\n\\begin{tikzpicture}\n")
    for node in g.nodes:
      for neighbor in node.neighbors:
        f.write("\t\\draw " + getEdgeString(node, neighbor))
    for node in g.nodes:
      f.write("\t\\draw " + getNodeString(node))   
    f.write("\end{tikzpicture}\n\end{document}")

