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
            
    def animate(self, dtheta):
        """Animate the crowd"""
        continu = True
        while continu:
            continu = False
            for indiv in self.individuals:
                V = VelocityField(indiv, self.tau)
                V.compute_field(self.tau, self.individuals)
                if S.Point(indiv.goal.x - indiv.position.x, indiv.goal.y - indiv.position.y) in V.field:
                    v = S.Point(indiv.goal.x - indiv.position.x, indiv.goal.y - indiv.position.y)
                else:
                    v = best_angle(V.field, S.Point(0, 0), self..tau, dtheta, indiv)
                
                if distance(indiv, goal) > 0.0001:
                    continu = True
                    # TODO : finish here
                else:
                    self.trajectory.add([goal.x,goal.y, 0.])
                    continue
