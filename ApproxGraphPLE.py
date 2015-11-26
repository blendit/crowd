import numpy as np
import math
import operator


class ApproxGraphPLE_Node:
    """Node from the approximation graph of the PLE algorithm"""
    # Nodes' coordinates
    x = float
    y = float
    z = float
    # State of the node in the graph
    disable = bool
    
    def __init__(self, x=0., y=0., z=0., disable=false):
        self.x = x
        self.y = y
        self.z = z
        self.disable = disable
        
        
class ApproxGraphPLE_Edge:
    """Edge from the approximation graph of the PLE algorithm"""
    # Min distance on the edge
    base_distance = float
    # Distance of the edge at time t
    distance = float
    
    def __init__(self, base_distance, node1, node2):
        self.base_distance = base_distance
        self.distance = base_distance
        self.nodes = [node1, node2]

Node = ApproxGraphPLE_Node
Edge = ApproxGraphPLE_Edge


class ApproxGraphPLE:
    """The class reprensenting the approximation graph for the PLE algorithm"""
  
    def __init__(self, dx=0., sizeX=0., sizeY=0., posX=0., posY=0.):
        self.nodes = []  # List of the nodes
        self.edges = {}
        self.dx = dx
        self.sizeX = sizeX.
        self.sizeY = sizeY
        self.posX = posX
        self.posY = posY
    
    def distance_euclidian(node1, node2):
        """Heuristic distance"""
        d = (node1.x - node2.x)**2 + (node1.y - node2.y)**2 + (node1.y - node2.y)**2
        d = math.sqrt(d)
        return d
    
    def distance(node1, node2):
        """Distance used in the A* algorithm"""
        distance_euclide(node1, node2)
    
    def add(self, node, edges):
        """Temporary way to add nodes"""
        self.nodes = self.nodes.append(node)
        self.edges[node] = edges
        
    def create(self):
        """Create a plan graph according to parameters"""
        node=Node()
    
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
            
            for (neighbor, edge) in self.edges[current]:
                if neighbor.disable:
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
