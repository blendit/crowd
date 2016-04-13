import numpy as np
import shapely.geometry as S
import math

import blendit.GraphPLE as G
import blendit.velocity_field as T
import blendit.geometric_tools as GT


class Individual:
    """The class independant from Blender describing an individual"""
    def __init__(self, x, y, z, vmax, vopt, es, ew, radius, goal):
        self.position = S.Point(x, y, z)
        self.position_new = S.Point(x, y, z)
        self.vmax = vmax
        self.vopt = vopt
        # See the PLEdestrian paper for the meaning of this notations
        self.es = es
        self.ew = ew
        self.v = S.Point(0, 0, 0)
        self.v_new = S.Point(0, 0)
        self.radius = radius
        self.trajectory = [[x, y, z]]
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

    def animate(self, dtheta, N, minefield):
        """Animate the crowd"""
        continu = True
        count = 0
        while continu and (count <= N or N == -1):
            count += 1
            continu = False
            for indiv in self.individuals:
                print("#########################", count, "\nNext:")
                V = T.VelocityField(indiv, self.tau)
                V.compute_field(self.tau, self.individuals, minefield)
                print("Field :", V.field)

                if V.field.is_empty:
                    v = S.Point(0, 0)
                else:
                    p = S.Point((indiv.goal.x - indiv.position.x) / self.tau, (indiv.goal.y - indiv.position.y) / self.tau)
                    if V.field.intersection(S.Point(0, 0).buffer(indiv.vopt)).contains(p):
                        v = S.Point((indiv.goal.x - indiv.position.x) / self.tau, (indiv.goal.y - indiv.position.y) / self.tau)
                        print("Fin ?")
                    elif V.field.intersection(S.Point(0, 0).buffer(indiv.vmax)).contains(p):
                        norm = GT.distance(p, S.Point(0, 0))
                        v = S.Point((indiv.goal.x - indiv.position.x) * indiv.vopt / norm / self.tau, (indiv.goal.y - indiv.position.y) * indiv.vopt / norm / self.tau)
                        print("Presque Fin ?")
                    else:
                        v = GT.best_angle(indiv.vopt, V.field, S.Point(0, 0), self.tau, dtheta, indiv, indiv.goal, self.graph)

                print("\tvitesse : ", v, "\n\t indiv :", indiv.position, "\n\t goal :", indiv.goal)

                indiv.v_new = v
                indiv.position_new = S.Point(indiv.position.x + v.x * self.tau, indiv.position.y + v.y * self.tau, indiv.position.z)
                indiv.trajectory.extend([[indiv.position_new.x, indiv.position_new.y, indiv.position_new.z]])
                if GT.distance(indiv.position, indiv.goal) > 0.1:
                    continu = True

            for indiv in self.individuals:
                indiv.v = indiv.v_new
                indiv.position = indiv.position_new

    def to_list_of_point(self):
        points = list()
        for indiv in self.individuals:
            points.extend([indiv.trajectory])
        return points
