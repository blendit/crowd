import numpy as np
import math
import operator

class ApproxGraphPLE_Node:
    """Node from the approximation graph of the PLE algorithm"""
    x = float
    y = float
    z = float
    disable = bool
    
    def __init__(self, x, y, z, disable):
        self.x = x
        self.y = y
        self.z = z
        self.disable = disable
        
class ApproxGraphPLE_Edge:
    """Edge from the approximation graph of the PLE algorithm"""
    base_distance = float
    distance = float
    
    def __init__(self, base_distance, node1, node2):
        self.base_distance = base_distance
        self.distance = base_distance
        self.nodes = [node1, node2]

Node = ApproxGraphPLE_Node
Edge = ApproxGraphPLE_Edge

class ApproxGraphPLE:
    """The class reprensenting the approximation graph for the PLE algorithm"""
    def __init__(self):
        self.nodes = []
        self.edges = {}
    
    def distance_euclidian(node1, node2):
        d = (node1.x - node2.x)**2 + (node1.y - node2.y)**2 + (node1.y - node2.y)**2
        d = math.sqrt(d)
        return d
        
    def distance(node1, node2):
        distance_euclide(node1, node2)
        
    def add(self, node, edges):
        self.nodes = self.nodes.append(node)
        self.edges[node] = edges
        
    def smallest_path_a_star(self, start, goal):
        to_evaluate = {start: distance(start, goal)}
        score = {start: 0. }
        seen = {}
        
        while len(to_evaluate) > 0:
            current = min(to_evaluate.items(), key=operator.itemgetter(1))[0]  # Get the minimum node of to_evaluate
            if current == goal:
                return score[goal]
                
            to_evaluate.pop(current)
            seen[current] = 1
            
            for neighbor, edge in self.edges[current].items():
                if seen.has_key(neighbor):
                    continue
                local_score = score[current] + edge.distance
                if to_evaluate.has_key(neighbor):
                    if local_score > score[neighbor]:
                        continue
                
                to_evaluate[neighbor] = local_score + distance(neighbor,goal)
                score[neighbor] = local_score
    
