import numpy as np
import shapely.geometry as S
import math

import GraphPLE as G
import classes as C
import geometric_tools as GT

es = 2.23
ew = 1.26

ind1 = C.Individual(0, 0, 0, 5, 2, es, ew, 2, S.Point(40, 50))
ind2 = C.Individual(40, 50, 0, 5, 2, es, ew, 2, S.Point(0, 0))

graph = G.Graph(d=0.5, sizeX=100, sizeY=100, posX=0, posY=0)

cr = C.Crowd(graph, 0.5)

cr.add_indiv(ind1)
cr.add_indiv(ind2)


cr.animate(0.1)

print(cr.to_list_of_point())
