import math


class Node:
    """Node from the approximation graph of the PLE algorithm"""
    def __init__(self, x=0., y=0., z=0., disable=False):
        self.x = x
        self.y = y
        self.z = z
        self.disable = disable
        
        
class Edge:
    """Edge from the approximation graph of the PLE algorithm"""
    def __init__(self, base_distance, node1, node2, disable=False):
        self.base_distance = base_distance
        self.distance = base_distance
        self.nodes = [node1, node2]
        self.disable = disable


class Graph:
    """The class reprensenting the approximation graph for the PLE algorithm"""
  
    def __init__(self, dx=0., sizeX=0., sizeY=0., posX=0., posY=0.):
        self.nodes = []  # List of the nodes
        self.edges = {}
        self.dx = dx
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.posX = posX
        self.posY = posY
        self.nX = 0
        self.nY = 0
    
    def distance_euclidian(node1, node2):
        """Heuristic distance"""
        d = (node1.x - node2.x)**2 + (node1.y - node2.y)**2 + (node1.y - node2.y)**2
        d = math.sqrt(d)
        return d
    
    def distance(node1, node2):
        """Distance used in the A* algorithm"""
        distance_euclide(node1, node2)
        
    def create(self, sizeX, sizeY, d, posX, posY, base_distance):
        """Create a grid plane graph according to parameters"""
        self.nX = math.floor(sizeX / d) + 1
        self.nY = math.floor(sizeY / d) + 1
        self.nodes = [Node()]
        self.edges = {}
        for i in range(0, self.nX - 1):
            for j in range(0, self.nY - 1):
                self.nodes.append(Node(x=posX + d * i, y=posY + d * j))
        for i in range(0, self.nX - 1):
            for j in range(0, self.nY - 1):
                self.edges[self.node[1 + i + j * self.sizeX]] = {}
                my_node = self.node[1 + i + j * self.sizeX]
                my_neighboors = self.edge[my_node]
                if i > 0:
                    neighboor = self.node[i + j * self.sizeX]
                    my_neighboors[neighboor] = Edge(base_distance, my_node, neighboor)
                if i < self.nX - 1:
                    neighboor = self.node[2 + i + j * self.sizeX]
                    my_neighboors[neighboor] = Edge(base_distance, my_node, neighboor)
                if j > 0:
                    neighboor = self.node[1 + i + (j - 1) * self.sizeX]
                    my_neighboors[neighboor] = Edge(base_distance, my_node, neighboor)
                if j < self.nY - 1:
                    neighboor = self.node[i + (j + 1) * self.sizeX]
                    my_neighboors[neighboor] = Edge(base_distance, my_node, neighboor)
                self.edges[my_node] = my_neighboors

    def find_neighboors(posX, posY):
        """Find the nodes of the grid the closest to this position"""

    def add_entry_point(self, posX, posY, posZ=0., base_distance):
        """Add the individual in the graph"""
        my_neighboors = self.find_neighboors(posX, posY)
        me = Node(x=posX, y=posY, z=posZ)
        self.nodes[0] = me
        for neighnoor in my_neighboors:
            new_edge = Edge(base_distance, me, neighboor)
            self.edges[me][neighboor] = new_edge
            self.edges[neighboor][me] = new_edge
    
    def remove_entry_point(self):
        """Remove the individual position"""
        indiv = self.nodes[0]
        for neighboor, edge in self.edges[indiv].items():
            del self.edges[neighboor][indiv]
        del self.edges[indiv]
            
    def smallest_path_a_star(self, start, goal):
        """A* algorithm"""
        to_evaluate = {start: distance(start, goal)}  # Dictionary of the nodes to evaluate and the approximated distance to the goal
        score = {start: 0.}  # Distance to the goal
        seen = {}  # Dictionary of the node seen
        
        while len(to_evaluate) > 0:
            current = min(to_evaluate.items(), key=operator.itemgetter(1))[0]  # Get the minimum node of to_evaluate
            if current == goal:  # It is over
                return score[goal]
                
            to_evaluate.pop(current)
            seen[current] = 1  # Adding current into the dictionary (the value doesn't interest us)
            
            for (neighbor, edge) in self.edges[current].items():
                if neighbor.disable or edge.disable:
                    continue
                if neighbor in seen:
                    continue
                local_score = score[current] + edge.distance  # Posible minimum distance to the start
                if neighbor in to_evaluate:
                    if local_score >= score[neighbor]:
                        continue
                
                to_evaluate[neighbor] = local_score + distance(neighbor, goal)  # Distance so far + heuristic distance
                score[neighbor] = local_score
        # Error -> TODO
