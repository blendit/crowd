import math


class Node:
    """Node from the approximation graph of the PLE algorithm"""
    def __init__(self, x=0., y=0., z=0., disable=False):
        self.x = x
        self.y = y
        self.z = z
        self.disable = disable
        # Two atributes used in the A* algorithm in order to reduce memory consumption.
        self.seen = False
        self.score = 0.

    def distance_euclidian(self, node2):
        """Heuristic distance"""
        d = (self.x - node2.x)**2 + (self.y - node2.y)**2 + (self.z - node2.z)**2
        d = math.sqrt(d)
        return d
        

def distance(node1, node2):
    """Distance used in the A* algorithm"""
    return node1.distance_euclidian(node2)
        
        
class Edge:
    """Edge from the approximation graph of the PLE algorithm"""
    def __init__(self, base_distance, node1, node2, disable=False):
        self.base_distance = base_distance
        self.distance = base_distance
        self.nodes = [node1, node2]
        self.disable = disable
        self.influence = 0
        
    def base_distance_gen(self, coef=1.):
        self.base_distance = distance(self.nodes[0], self.nodes[1]) * coef
        
    def base_distance_set(self, base_distance):
        self.base_distance = base_distance
        
    def init_distance(self):
        self.distance = self.base_distance


class Graph:
    """The class reprensenting the approximation graph for the PLE algorithm"""
    def __init__(self, d=0., sizeX=0., sizeY=0., posX=0., posY=0.):
        self.nodes = []  # List of the nodes
        self.edges = {}
        self.d = d
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.posX = posX
        self.posY = posY
        self.nX = 0
        self.nY = 0
        
    def default_calc_base_distance(edge):
        edge.base_distance_gen()
        
    def create(self, calc_base_distance=default_calc_base_distance):
        """Create a grid plane graph according to parameters"""
        self.nX = math.floor(self.sizeX / self.d) + 1
        self.nY = math.floor(self.sizeY / self.d) + 1
        self.nodes = [Node()]
        self.edges = {}
        for j in range(0, self.nY):
            for i in range(0, self.nX):
                self.nodes.append(Node(x=self.posX + self.d * i, y=self.posY + self.d * j))
        for i in range(0, self.nX):
            for j in range(0, self.nY):
                self.edges[self.nodes[1 + i + j * self.nX]] = {}
        for i in range(0, self.nX):
            for j in range(0, self.nY):
                my_node = self.nodes[1 + i + j * self.nX]
                my_neighbors = self.edges[my_node]
                if i < self.nX - 1:
                    neighbor = self.nodes[2 + i + j * self.nX]
                    new_edge = Edge(0., my_node, neighbor)
                    my_neighbors[neighbor] = new_edge
                    self.edges[neighbor][my_node] = new_edge
                    calc_base_distance(my_neighbors[neighbor])
                    my_neighbors[neighbor].init_distance()
                if j < self.nY - 1:
                    neighbor = self.nodes[1 + i + (j + 1) * self.nX]
                    new_edge = Edge(0., my_node, neighbor)
                    my_neighbors[neighbor] = new_edge
                    self.edges[neighbor][my_node] = new_edge
                    calc_base_distance(my_neighbors[neighbor])
                    my_neighbors[neighbor].init_distance()
                if i < self.nX - 1 and j > 0:
                    neighbor = self.nodes[2 + i + (j - 1) * self.nX]
                    new_edge = Edge(0., my_node, neighbor)
                    my_neighbors[neighbor] = new_edge
                    self.edges[neighbor][my_node] = new_edge
                    calc_base_distance(my_neighbors[neighbor])
                    my_neighbors[neighbor].init_distance()
                if j < self.nY - 1 and i < self.nX - 1:
                    neighbor = self.nodes[2 + i + (j + 1) * self.nX]
                    new_edge = Edge(0., my_node, neighbor)
                    my_neighbors[neighbor] = new_edge
                    self.edges[neighbor][my_node] = new_edge
                    calc_base_distance(my_neighbors[neighbor])
                    my_neighbors[neighbor].init_distance()
                self.edges[my_node] = my_neighbors

    def find_neighbors(self, x, y):
        """Find the nodes of the grid the closest to this position"""
        neighbors = []
        px = x - self.posX
        py = y - self.posY
        dx = px / self.d
        dy = py / self.d
        neighbor_se_idx = min(self.nX - 1, math.floor(dx))
        neighbor_se_idy = min(self.nY - 1, math.floor(dy))
        if neighbor_se_idx >= 0 and neighbor_se_idy >= 0 and neighbor_se_idx <= self.nX - 1 and neighbor_se_idy <= self.nY - 1:
            neighbors.append(self.nodes[1 + neighbor_se_idx + neighbor_se_idy * self.nX])
        if neighbor_se_idx + 1 >= 0 and neighbor_se_idy >= 0 and neighbor_se_idx + 1 <= self.nX - 1 and neighbor_se_idy <= self.nY - 1:
            neighbors.append(self.nodes[2 + neighbor_se_idx + neighbor_se_idy * self.nX])
        if neighbor_se_idx >= 0 and neighbor_se_idy + 1 >= 0 and neighbor_se_idx <= self.nX - 1 and neighbor_se_idy + 1 <= self.nY - 1:
            neighbors.append(self.nodes[1 + neighbor_se_idx + (neighbor_se_idy + 1) * self.nX])
        if neighbor_se_idx + 1 >= 0 and neighbor_se_idy + 1 >= 0 and neighbor_se_idx + 1 <= self.nX - 1 and neighbor_se_idy + 1 <= self.nY - 1:
            neighbors.append(self.nodes[2 + neighbor_se_idx + (neighbor_se_idy + 1) * self.nX])
        return neighbors

    def add_entry_point(self, posX, posY, posZ=0.):
        """Add the individual in the graph"""
        my_neighbors = self.find_neighbors(posX, posY)
        me = Node(x=posX, y=posY, z=posZ)
        self.nodes[0] = me
        self.edges[me] = {}
        for neighbor in my_neighbors:
            # print('voisin : (%.2f,%.2f)' %(neighbor.x,neighbor.y))
            new_edge = Edge(0., me, neighbor)
            new_edge.base_distance_gen()
            new_edge.init_distance()
            self.edges[me][neighbor] = new_edge
            self.edges[neighbor][me] = new_edge
    
    def remove_entry_point(self):
        """Remove the individual position"""
        indiv = self.nodes[0]
        for neighbor in self.edges[indiv].keys():
            self.edges[neighbor].pop(indiv)
        self.edges.pop(indiv)
        
    def add_goal_point(self, posX, posY, posZ=0.):
        """Add the individual in the graph"""
        my_neighbors = self.find_neighbors(posX, posY)
        me = Node(x=posX, y=posY, z=posZ)
        self.nodes.append(me)
        self.edges[me] = {}
        for neighbor in my_neighbors:
            # print('voisin : (%.2f,%.2f)' %(neighbor.x,neighbor.y))
            new_edge = Edge(0., me, neighbor)
            new_edge.base_distance_gen()
            new_edge.init_distance()
            self.edges[me][neighbor] = new_edge
            self.edges[neighbor][me] = new_edge
    
    def remove_goal_point(self):
        """Remove the individual position"""
        goal = self.nodes[1 + self.nX * self.nY]
        for neighbor in self.edges[goal].keys():
            self.edges[neighbor].pop(goal)
        self.edges.pop(goal)
            
    def smallest_path_a_star(self):
        """A* algorithm"""
        start = self.nodes[0]
        goal = self.nodes[1 + self.nX * self.nY]
        to_evaluate = {start: distance(start, goal)}  # Dictionary of the nodes to evaluate and the approximated distance to the goal
        start.score = 0.  # Distance to the goal
        
        while len(to_evaluate) > 0:
            current = min(to_evaluate.items(), key=lambda x: x[1])[0]  # Get the minimum node of to_evaluate
            # print('Je vois (%.2f,%.2f) à %.2f' %(current.x,current.y,score[current]))
            
            if current == goal:  # It is over
                for node in self.nodes:
                    node.seen = False
                return goal.score
                
            to_evaluate.pop(current)
            current.seen = True  # Adding current into the dictionary (the value doesn't interest us)
            
            for (neighbor, edge) in self.edges[current].items():
                if neighbor.disable or edge.disable:
                    continue
                if neighbor.seen:
                    continue
                local_score = current.score + edge.distance  # Posible minimum distance to the start
                if neighbor in to_evaluate:
                    if local_score >= neighbor.score:
                        continue
                
                to_evaluate[neighbor] = local_score + distance(neighbor, goal)  # Distance so far + heuristic distance
                neighbor.score = local_score
        # Error -> TODO
