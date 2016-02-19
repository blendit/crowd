import numpy as np
import shapely.geometry as S
import math


def argument(point):
    """Gives the complex argument of a point in the plane"""
    return math.atan2(point.y, point.x)
   
 
def angle(p1, p2):
    """Gives the value of the angle represented by the two points as if they were vectors. The value is in [0, 2*Pi]"""
    theta1 = argument(p1)
    theta2 = argument(p2)
    theta = theta2 - theta1
    while theta < 0:
        theta += 2 * math.pi
    while theta > 2 * math.pi:
        theta -= 2 * math.pi
    return theta


def difference(p1, p2):
    """Make the substraction of two points as if they were vectors"""
    return S.Point(p1.x - p2.x, p1.y - p2.y)


def distance(point1, point2):
    """Euclidian Distance between two points"""
    d = (point1.x - point2.x)**2 + (point1.y - point2.y)**2
    d = math.sqrt(d)
    return d


def distance_tuple(point1, point2):
    """Euclidian Distance between two points"""
    d = (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2
    d = math.sqrt(d)
    return d
    
 
def point_to_tuple(point):
    """Transform a list of Points into a list of tuples"""
    return (point.x, point.y)


def find_projection_segment(pA, pB, pM):
    """Find the closest point on the segment [AB] to the point M"""
    # Compute vector AB and AM
    vectAB = (pB[0] - pA[0], pB[1] - pA[1])
    if vectAB == (0, 0):
        return pA  # Special case
    vectAM = (pM[0] - pA[0], pM[1] - pA[1])
    
    # Find the scalar product between the two
    scalar = vectAB[0] * vectAM[0] + vectAB[1] * vectAM[1]
    # Compute the norm of AB
    dist_square = vectAB[0] * vectAB[0] + vectAB[1] * vectAB[1]
    
    # Return the point
    if 0 > scalar:
        return pA  # Outside of the segment
    elif scalar > dist_square:
        return pB  # Outside of the segment
    else:
        scalar = scalar / dist_square
        return (pA[0] + vectAB[0] * scalar, pA[1] + vectAB[1] * scalar)  # The actual projection point


def find_projection_half_line(pA, pB, pM):
    """Find the closest point on the half line { x in plane | x not in [AB) and x in (AB) } to the point M. In words the half line is given by pA which is the starting point and by pB which indicates the line (AB) but we take the half line going into the opposite direction"""
    # Compute vector AB and AM
    vectAB = (pB[0] - pA[0], pB[1] - pA[1])
    if vectAB == (0, 0):
        return pA  # Special case
    vectAM = (pM[0] - pA[0], pM[1] - pA[1])
    
    # Find the scalar product between the two
    scalar = vectAB[0] * vectAM[0] + vectAB[1] * vectAM[1]
    # Compute the norm of AB
    dist_square = vectAB[0] * vectAB[0] + vectAB[1] * vectAB[1]
    
    # Return the point
    if scalar < 0:
        scalar = scalar / dist_square
        return (pA[0] + vectAB[0] * scalar, pA[1] + vectAB[1] * scalar)
    else:
        return pA
        
        
class TruncatedCone:
    """Represent the truncated cone"""
    
    def __init__(self, pA, rA, pB, rB, dmax, tau):
        """Create a truncated cone for the ORCA algorithm"""
        
        # Usefull geometric datas
        center = S.Point(pB.x - pA.x, pB.y - pA.y)
        theta_c = argument(center)
        norm = distance(center, S.Point(0, 0))
        r = rA + rB
        
        if norm > 0:
            # Trigonometric formulas
            cos_theta = math.sqrt(norm ** 2 - r ** 2) / norm
            sin_theta = r / norm
            
            norm2 = math.sqrt(norm ** 2 - r ** 2) / tau
            
            # Define the two limits point
            point1 = S.Point(norm2 * (math.cos(theta_c) * cos_theta + sin_theta * math.sin(theta_c)), norm2 * (math.sin(theta_c) * cos_theta - sin_theta * math.cos(theta_c)))
            point2 = S.Point(norm2 * (math.cos(theta_c) * cos_theta - sin_theta * math.sin(theta_c)), norm2 * (math.sin(theta_c) * cos_theta + sin_theta * math.cos(theta_c)))
            
        else:
            raise Blendit('Same Position Between Two Peaple')
        
        self.limit_points = [point1, point2]

        # Define the arc
        center = S.Point(center.x / tau, center.y / tau)
        radius = r / tau
        start_angle = argument(difference(point1, center))
        end_angle = argument(difference(point2, center))
        numsegments = 65

        # We format the angle so that we get the smaller one of the two possible
        if start_angle - end_angle > math.pi:
            start_angle -= 2 * math.pi
        if start_angle - end_angle < -math.pi:
            start_angle += 2 * math.pi

        # The coordinates of the arc
        theta = np.linspace(start_angle, end_angle, numsegments)
        x = center.x + radius * np.cos(theta)
        y = center.y + radius * np.sin(theta)
        
        # The arc
        self.arc = S.LineString(np.column_stack([x, y]))

    def find_closest(self, point):
        """Find the closest point of the boundaries of our truncated cone to the point passed as second parameter"""
        # We get back the list of vertices
        point_list = list(self.arc.coords)
        
        # We compute the projection on the first half line
        minimum = [find_projection_half_line(point_to_tuple(self.limit_points[0]), (0, 0), point)]
        minimum.append(distance_tuple(point, minimum[0]))
        
        # And the second
        proj = find_projection_half_line(point_to_tuple(self.limit_points[1]), (0, 0), point)
        dist = distance_tuple(point, proj)
        if dist < minimum[1]:
                minimum = [proj, dist]
        
        # For each segment within the list we check the projection
        for i in range(len(point_list) - 1):
            first = point_list[i]
            second = point_list[i + 1]
            
            proj = find_projection_segment(first, second, point)
            dist = distance_tuple(point, proj)
            
            if dist < minimum[1]:
                minimum = [proj, dist]
        
        # We return the result
        return S.Point(minimum[0][0], minimum[0][1])
        

# Non tested/corrected stuff at the moment

def in_half_plane(origin, orthogonal, point):
    if (point.x - origin.x) * orthogonal.x + (point.y - origin.y) * orthogonal.y >= -0.000001:
        return True
    return False
   
    
def intersection_line_line(origin1, ortho, point1, point2, vmax):
    """This function makes an intersection between two lines with the following representations:
    line1 : origin1 + ortho (vector that is normal to the line)
    line2 : two points
    """
    vect1 = S.Point(point1.x - point2.x, point1.y - point2.y)
    if vect1.x * ortho.x + vect1.y * ortho.y == 0:
        return []
    origin2 = S.Point(origin1.x + ortho.y, origin1.y - ortho.x)
    px = (origin1.x * origin2.y - origin1.y * origin2.x) * (point1.x - point2.x) - (point1.x * point2.y - point1.y * point2.x) * (origin1.x - origin2.x)
    px /= (origin1.x - origin2.x) * (point1.y - point2.y) - (origin1.y - origin2.y) * (point1.x - point2.x)
    py = (origin1.y * origin2.x - origin1.x * origin2.y) * (point1.y - point2.y) - (point1.y * point2.x - point1.x * point2.y) * (origin1.y - origin2.y)
    py /= (origin1.y - origin2.y) * (point1.x - point2.x) - (origin1.x - origin2.x) * (point1.y - point2.y)
    print(px, py)
    if abs(px) <= vmax and abs(py) <= vmax:
        return [S.Point(px, py)]
    else:
        return []
    

def half_plane(origin, orthogonal, vmax):
    """Create the intersection of the half plane starting at point facing the direction given by orthogonal with the square  of 'radius' vmax"""
    end_points = [S.Point(-vmax, -vmax), S.Point(vmax, -vmax), S.Point(vmax, vmax), S.Point(-vmax, vmax)]  # Boundaries of the square
    points = []
    print("ortho :", orthogonal.x, orthogonal.y)
    print("####")
    print(origin.x, origin.y, orthogonal.x, orthogonal.y)
    for p in end_points:
        if in_half_plane(origin, orthogonal, p):
            print("ici")
            points.append(p)
    for i in range(4):
        for p in intersection_line_line(origin, orthogonal, end_points[i], end_points[(i + 1) % 4], vmax):
            print("ici'")
            points.append(p)
    points.sort(key=lambda x: argument(x))
    print([point_to_tuple(x) for x in points])
    return S.Polygon([point_to_tuple(x) for x in points])
