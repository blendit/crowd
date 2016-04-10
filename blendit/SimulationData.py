import blendit.GraphPLE as G
import blendit.classes as C
import blendit.geometric_tools as GT
import blendit.length_beziers.py as B

Individuals = []
graph = G.Graph(d=0.5, sizeX=100, sizeY=100, posX=0, posY=0)
es = 2.23
ew = 1.26
tau = 0.5
theta = 1
cr = C.Crowd(graph,tau)
N = 1
data = cr.to_list_of_points()
