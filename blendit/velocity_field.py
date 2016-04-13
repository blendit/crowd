import shapely.affinity as A
import shapely.geometry as S
import math
from blendit.geometric_tools import *


class VelocityField:
    """The class independant from Blender describing the allowed velocity fields"""
    def __init__(self, individual, tau):
        """Create the velocity field for the PLE algorithm"""
        # tau is the small movement time for which we compute the velocity field
        # others is a list of the others individuals (the first
        self.individual = individual  # individual whose velocity field is calculated
        self.init_field(tau)  # Base velocity field (square of sidelength 2 vmax * tau)

    def init_field(self, tau):
        """Create an initial velocity field for the individual"""
        vmax = self.individual.vmax  # Maximum velocity of the individual
        radius = vmax  # We compute the "radius" of the square
        self.field = S.Polygon([(- radius, - radius), (radius, - radius), (radius, radius), (-radius, radius)])

    def is_far_away(self, neighboor, tau):
        """Detect if two individuals are to far away to meet in the time tau"""
        dx = neighboor.position.x - self.individual.position.x
        dy = neighboor.position.y - self.individual.position.y
        dz = neighboor.position.z - self.individual.position.z
        distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        if distance > self.individual.vmax * tau + neighboor.vmax * tau + self.individual.radius + neighboor.radius:
            return True
        else:
            return False

    # TODO : Expend all of this to 3D situations
    def orca(self, neighboor, tau):
        """Computes the ORCA hyperplane between the two individual (cf Reciprocal n-body collision avoidance)"""
        # We define some parameters
        vmax = self.individual.vmax
        cas = 2
        epsilon = 0.05
        if cas == 1:
            v_opt = S.Point(0, 0)
        elif cas == 2:
            v_opt = difference(self.individual.v, neighboor.v)
        else:
            v_opt = difference(difference(neighboor.position, neighboor.goal), difference(self.individual.position, self.individual.goal))
            norm = distance(v_opt, S.Point(0, 0))
            if norm > 0:
                v_opt = S.Point(v_opt.x / norm * self.individual.vopt, v_opt.y / norm * self.individual.vopt)
        point_us = S.Point(self.individual.position.x, self.individual.position.y)
        point_him = S.Point(neighboor.position.x, neighboor.position.y)

        if distance(self.individual.position, neighboor.position) == self.individual.radius + neighboor.radius:
            return half_plane(S.Point(0, 0), difference(individual.position, neighboor.position), vmax)
        elif distance(self.individual.position, neighboor.position) < self.individual.radius + neighboor.radius:
            return S.Polygon([(-vmax, -vmax), (vmax, -vmax), (vmax, vmax), (-vmax, vmax)])

        # We create the trucated cone
        cone = TruncatedCone(point_us, self.individual.radius, point_him, neighboor.radius, vmax * tau, tau)

        # We get a point we have to find
        u_end = cone.find_closest((v_opt.x, v_opt.y))
        u = difference(u_end, v_opt)
        if cone.in_cone(v_opt):
            ortho = difference(u_end, v_opt)
        else:
            ortho = difference(v_opt, u_end)
        # u = ortho
        origin = S.Point((self.individual.v.x + 1.0 / 2.0 * u.x) * (1 - epsilon), (self.individual.v.y + 1.0 / 2.0 * u.y) * (1 - epsilon))
        print("ORCA:\n\torigin = ", origin, "\n\t u = ", u, "\n\t vA = ", self.individual.v, "\n\t vB = ", neighboor.v, "\n\t ortho =", ortho)
        # We return the right half plane
        return half_plane(origin, ortho, vmax)

    def compute_field(self, tau, others, minefield):  # TODO: This function has to be tested
        """This function computes a velocity_field for self.individual which is collision free with the others individuals"""
        for neighboor in others:
            if neighboor == self.individual:  # we only consider the others individual
                continue
            if self.is_far_away(neighboor, tau):   # we do not do computation for to far away individuals
                continue
            orc = self.orca(neighboor, tau).buffer(0)
            # if not self.field.is_empty and not orc.is_empty:
            self.field = self.field.intersection(orc).buffer(0)
        """
        for mine in minefield:
            if not mine.is_empty:
                epsilon = 0.
                mine_p = mine.buffer(self.individual.radius + epsilon)
                x, y = mine_p.exterior.xy
                minimum = float("inf")
                q = -1
                n = len(x)
                p_opt = S.Point(self.individual.position.x, self.individual.position.y)
                for i in range(len(x)):
                    p1 = (x[i], y[i])
                    p2 = (x[(i + 1) % n], y[(i + 1) % n])
                    p3 = find_projection_segment(p1, p2, (self.individual.position.x, self.individual.position.y))
                    if distance(p_opt, S.Point(p3[0], p3[1])) < minimum:
                        q = i
                        minimum = distance(p_opt, S.Point(p3[0], p3[1]))
                if n == 1 or q == -1:
                    continue
                p1 = (x[q], y[q])
                p2 = (x[(q + 1) % n], y[(q + 1) % n])
                p3 = find_projection_segment(p1, p2, (self.individual.position.x, self.individual.position.y))
                u = S.Point((-p_opt.x + p3[0]) / 2, (-p_opt.y + p3[1]) / 2)
                if mine_p.contains(p_opt):
                    ortho = u
                else:
                    ortho = S.Point(p_opt.x - p3[0], p_opt.y - p3[1])
                orc = half_plane(u, ortho, self.individual.vmax)
                self.field = self.field.intersection(orc)"""
