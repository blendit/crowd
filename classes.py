import numpy as np
import shapely.geometry as S
import math

import GraphPLE as G
import velocity_field as T
import geometric_tools as GT


class Individual:
    """The class independant from Blender describing an individual"""
    def __init__(self, x, y, z, vmax, vopt, es, ew, radius, goal):
        self.position = S.Point(x, y, z)
        self.vmax = vmax
        self.vopt = vopt
        # See the PLEdestrian paper for the meaning of this notations
        self.es = es
        self.ew = ew
        self.v = S.Point(0, 0, 0)
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
                V = T.VelocityField(indiv, self.tau)
                V.compute_field(self.tau, self.individuals, [])
                print(V.field)
                
                if S.Point((indiv.goal.x - indiv.position.x) / self.tau, (indiv.goal.y - indiv.position.y) / self.tau) in V.field.exterior.coords:
                    v = S.Point((indiv.goal.x - indiv.position.x) / self.tau, (indiv.goal.y - indiv.position.y) / self.tau)
                    print("bla")
                else:
                    v = GT.best_angle(indiv.vopt, V.field, S.Point(0, 0), self.tau, dtheta, indiv, indiv.goal)
                print(v.x, v.y, indiv.position, indiv.goal)
                indiv.v = v
                if GT.distance(indiv.position, indiv.goal) > 0.1:
                    continu = True
                    indiv.position = S.Point(indiv.position.x + v.x * self.tau, indiv.position.y + v.y * self.tau, indiv.position.z)
                    indiv.trajectory.extend([[indiv.position.x, indiv.position.y, indiv.position.z]])
                    print("cas1", indiv.position.x + v.x * self.tau, indiv.position.y + v.y * self.tau)
                    # TODO : finish here
                else:
                    indiv.position = S.Point(indiv.goal.x, indiv.goal.y, indiv.position.z)
                    indiv.trajectory.extend([[indiv.goal.x, indiv.goal.y, indiv.position.z]])
                    print("cas2", indiv.goal.x, indiv.goal.y)
                    continue
                    
    def to_list_of_point(self):
        points = list()
        for indiv in self.individuals:
            points.extend([indiv.trajectory])
        return points
