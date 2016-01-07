import shapely.geometry as S
import math

class VelocityField:
    """The class independant from Blender describing the allowed velocity fields"""
    def __init__(self, individual, tau, others):
        """Create the velocity field for the PLE algorithm"""
        # tau is the small movement time for which we compute the velocity field
        # others is a list of the others individuals (the first 
        self.individual = individual # individual whose velocity field is calculated
        self.init_field(dt) # Base velocity field (square of sidelength 2 vmax * tau)
        
    def init_field(self, tau):
        """Create an initial velocity field for the individual"""
        vmax = self.individual.vmax # Maximum velocity of the individual
        radius = vmax * tau # We compute the "radius" of the square
        self.field = S.Polygon([(- radius, - radius), (radius, - radius), (- radius, radius), (radius, radius)])
        
    def is_far_away(self, neighboor, tau):
        """Detect if two individuals are to far away to meet in the time tau"""
        dx = neighboor.x - self.individual.x
        dy = neighboor.y - self.individual.y
        dz = neighboor.z - self.individual.z
        distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        if distance > individual.vmax * tau + neighboor.vmax * tau + individual.radius + neighboor.radius:
            return True
        else:
            return False
    
    def compute_field(self, tau, others):
        """This function computes a velocity_field for self.individual which is collision free with the others individuals"""
        for neighboor in others:
            if neighboor == individual: # we only consider the others individual
                continue
            if is_far_away(neighboor):  # we do not do computation for to far away individuals
                continue
            # TODO : call a function that effectively compute the velocity field
            
