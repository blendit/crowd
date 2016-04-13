import blendit.GraphPLE as G
import blendit.classes as C
import blendit.geometric_tools as GT
import shapely.geometry as Sha

Individuals = []

MinGrid = 0.1
# Maxgrid = Mingrid*10^5
Grid = 5
OriginX = 0
OriginY = 0
MaxX = 10
MaxY = 10
MinX = -10
MinY = -10

graph = G.Graph(d=Grid,
                sizeX=MaxX-MinX,
                sizeY=MaxY-MinY,
                posX=OriginX+MinX,
                posY=OriginY+MinY)


def renew_graph():
    graph = G.Graph(d=Grid,
                    sizeX=MaxX-MinX,
                    sizeY=MaxY-MinY,
                    posX=OriginX+MinX,
                    posY=OriginY+MinY)

es = 2.23
ew = 1.26
tau = 1
theta = 1
cr = C.Crowd(graph, tau)


def reset_crowd(crowd):
    crowd = C.Crowd(graph, tau)

    
N = -1
data = cr.to_list_of_point()
minefield = []
