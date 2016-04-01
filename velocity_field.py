import shapely.geometry as S
import math
from geometric_tools import *


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
        radius = vmax * tau  # We compute the "radius" of the square
        self.field = S.Polygon([(- radius, - radius), (radius, - radius), (- radius, radius), (radius, radius)])
        
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
        point_us = S.Point(self.individual.position.x, self.individual.position.y)
        point_him = S.Point(neighboor.position.x, neighboor.position.y)
        
        if distance(self.individual.position, neighboor.position) == self.individual.radius + neighboor.radius:
            return half_plane(Point(0,0), v_opt, vmax)
        elif distance(self.individual.position, neighboor.position) < self.individual.radius + neighboor.radius:
            return S.Polygon([(-vmax,-vmax), (vmax, -vmax), (vmax, vmax), (-vmax, vmax)])
        
        v_opt = difference(self.individual.v, neighboor.v)
        
        # We create the trucated cone
        cone = TruncatedCone(point_us, self.individual.radius, point_him, neighboor.radius, vmax * tau, tau)
        # We get a point we have to find
        u_end = cone.find_closest((v_opt.x, v_opt.y))
        
        u = difference(u_end, v_opt)
        origin = S.Point(self.individual.v.x + 1.0 / 2.0 * u.x, self.individual.v.y + 1.0 / 2.0 * u.y)
        print("half ", origin, u, vmax, u_end, v_opt)
        # We return the right half plane
        return half_plane(origin, u, vmax)

    def compute_field(self, tau, others, minefield):  # TODO: This function has to be tested
        """This function computes a velocity_field for self.individual which is collision free with the others individuals"""
        for neighboor in others:
            if neighboor == self.individual:  # we only consider the others individual
                continue
            if self.is_far_away(neighboor, tau):   # we do not do computation for to far away individuals
                continue
            orc = self.orca(neighboor, tau)
            print(orc)
            self.field = self.field.intersection(orc)
        for mine in minefield:
            self.field = self.field.difference(mine)
        # TODO : Take the environment into account
