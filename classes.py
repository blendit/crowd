import numpy as np
import shapely.geometry as S
import math


class Individual:
    """The class independant from Blender describing an individual"""
    def __init__(self, x, y, z, vmax, vopt, es, ew, radius, goal):
        self.position = S.Point(x, y, z)
        self.vmax = vmax
        self.vopt = vopt
        # See the PLEdestrian paper for the meaning of this notations
        self.es = es
        self.ew = ew
        self.radius = radius
        self.trajectory = list()
        self.goal = goal


class Crowd:
    """The class independant from Blender describing the crowd"""
    def __init__(self, graph, tau):
        self.individuals = set()
        self.graph = graph
        self.tau = tau
    
    def add_indiv(self, indiv):
        """Add one individual to the crowd"""
        self.individuals.add(indiv)
            
    def animate(self):
        """Animate the crowd"""
        continu = True
        while continu:
            continu = False
            for indiv in self.individuals:
                
