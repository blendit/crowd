import blendit.GraphPLE as G
import blendit.classes as C
import blendit.geometric_tools as GT
import shapely.geometry as Sha

Individuals = []

MinGrid = 0.5
# Maxgrid = Mingrid*10^5
Grid = 0.5
OriginX = 0
OriginY = 0
MaxX = 100
MaxY = 100
MinX = 0
MinY = 0
taille = 30
radius = 1.1

graph = G.Graph(d=Grid,
                sizeX=MaxX - MinX,
                sizeY=MaxY - MinY,
                posX=OriginX + MinX,
                posY=OriginY + MinY)




es = 2.23
ew = 1.26
tau = 1
theta = 0.05
cr = C.Crowd(graph, tau)




    
N = -1
data = cr.to_list_of_point()
minefield = []
