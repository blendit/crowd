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
    
 
def point_to_tuple(point_list):
    """Transform a list of Points into a list of tuples"""
    liste = []
    for p in point_list:
        liste.append((p.x, p.y))
    return liste

    
def create_cone(point1, point2, dmax):
    """Create a polygon representing a cone.
It starts at (0,0) and the 2 limits of the cone are given by the two points, the angle is also supposed smaller than Pi. We can see the points as vectors defining the two half lines of the cone.
Moreover this cone is intersected with a square given by dmax"""
    # We compute the angle between the two boundary points
    theta_ref = angle(point1, point2)
    vertices = []  # Our cone
    # We add the intersections of the two half line [0, point1) and [0, point2) with the square
    z = max(abs(point1.x), abs(point1.y))
    vertices.append(S.Point(point1.x / z * dmax, point1.y / z * dmax))
    z = max(abs(point2.x), abs(point2.y))
    vertices.append(S.Point(point2.x / z * dmax, point2.y / z * dmax))
    # Boundaries of the square
    end_points = [S.Point(-dmax, -dmax), S.Point(dmax, -dmax), S.Point(dmax, dmax), S.Point(-dmax, dmax)]
    # We start looking for the corners of the square that are in the cone
    for p in end_points:
        theta = angle(point1, p)
        # This test is true if the point p is in the cone
        if 0 <= theta and theta <= theta_ref:
            vertices.append(p)
    # We put the vertices in the right order
    vertices.sort(key=lambda x: angle(point1, x))
    vertices.append(S.Point(0, 0))
    return S.Polygon(point_to_tuple(vertices))
 
   
def cut_cone(cone, center, radius, dmax):
    """Create a truncated cone for the ORCA algorithm given the cone and a circle.
To create this truncated cone, we need to first to cut a triangle consisting of the point 0 and the two points of the circle who make a diameter perpandicular to the segment [0,center of the circle].
We then add back the disk induced by the circle.
    """
    disk_plus = center.buffer(radius)  # the disk to add
    disk_minus = S.Point(0, 0).buffer(math.sqrt(distance(center, S.Point(0, 0)) ** 2 - radius ** 2))  # the disk that will cut the triangle (it will cut more but this will be added back at the union step
    result = cone.difference(disk_minus)  # We cut a part of the cone
    result = result.union(disk_plus)  # We add back another part
    square = S.Polygon([(-dmax, -dmax), (dmax, -dmax), (dmax, dmax), (-dmax, dmax)])
    result = result.intersection(square)  # we make sure that we didn't add too much
    return result


class alternative_truncated_cone:
    """Represent the truncated cone"""
    
    def __init__(self, pA, rA, pB, rB, dmax, tau):
        """Create a truncated cone for the ORCA algorithm"""
        center = S.Point(pB.x - pA.x, pB.y - pA.y)
        theta_c = argument(center)
        norm = distance(center, S.Point(0, 0))
        r = rA + rB
        if norm > 0:
            cos_theta = math.sqrt(norm ** 2 - r ** 2) / norm
            sin_theta = r / norm
            norm /= tau
            # Trigonometric formulas
            point1 = S.Point(norm * (math.cos(theta_c) * cos_theta + sin_theta * math.sin(theta_c)), norm * (math.sin(theta_c) * cos_theta - sin_theta * math.cos(theta_c)))
            point2 = S.Point(norm * (math.cos(theta_c) * cos_theta - sin_theta * math.sin(theta_c)), norm * (math.sin(theta_c) * cos_theta + sin_theta * math.cos(theta_c)))
        else:
            raise Blendit('Same Position Between Two Peaple')
        self.limit_points = [point1, point2]
        center = S.Point(center.x / tau, center.y / tau)
        other_point = S.Point(2 * center.x, 2 * center.y)
        cut_triangle = S.Polygon([(other_point.x, other_point.y), (point1.x, point1.y), (point2.x, point2.y)])
        disk = center.buffer((rA + rB) / tau)
        half_disk = disk.intersection(cut_triangle)
        # TODO : transform half_disk into half_circle.


def create_truncate_cone(pA, rA, pB, rB, dmax, tau):
    """Create a truncated cone for the ORCA algorithm"""
    # We first need to find the two points for the create_cone function
    center = S.Point(pB.x - pA.x, pB.y - pA.y)
    theta_c = argument(center)
    norm = distance(center, S.Point(0, 0))
    r = rA + rB
    if norm > 0:
        cos_theta = math.sqrt(norm ** 2 - r ** 2) / norm
        sin_theta = r / norm
        norm /= tau
        # Trigonometric formulas
        point1 = S.Point(norm * (math.cos(theta_c) * cos_theta + sin_theta * math.sin(theta_c)), norm * (math.sin(theta_c) * cos_theta - sin_theta * math.cos(theta_c)))
        point2 = S.Point(norm * (math.cos(theta_c) * cos_theta - sin_theta * math.sin(theta_c)), norm * (math.sin(theta_c) * cos_theta + sin_theta * math.cos(theta_c)))
    else:
        raise Blendit('Same Position Between Two Peaple')
    # We compute the cone
    cone = create_cone(point1, point2, dmax)
    center = S.Point(center.x / tau, center.y / tau)
    # We truncate the cone
    cone = cut_cone(cone, center, (rA + rB) / tau, dmax)
    # TODO : Add point1/tau and point2/tau in the return
    return [cone, point1, point2]


def find_projection(pA, pB, pM):
    """Find the closest point on the segment [AB] to the point M"""
    # TODO : This is not working at all
    """
    dist = math.sqrt((pB[0] - pA[0]) ** 2 + (pB[1] - pA[1]) ** 2)
    AM = (pM[0] - pA[0]) * (pB[0] - pA[0]) + (pM[1] - pA[1]) * (pB[1] - pA[1])
    AM /= dist
    x, y = pM[0] + AM / dist * (pB[0] - pA[0]), pM[1] + AM / dist * (pB[1] - pA[1])
    scalar = (x - pA[0]) * (pB[0] - pA[0]) + (y - pA[1]) * (pB[1] - pA[1])
    """
    vectAB = (pB[0] - pA[0], pB[1] - pA[1])
    if vectAB == (0, 0):
        return pA
    vectAM = (pM[0] - pA[0], pM[1] - pA[1])
    scalar = vectAB[0] * vectAM[0] + vectAB[1] * vectAM[1]
    dist_square = vectAB[0] * vectAB[0] + vectAB[1] * vectAB[1]
    if 0 > scalar:
        return pA
    elif scalar > dist_square:
        return pB
    else:
        scalar = scalar / dist_square
        return (pA[0] + vectAB[0] * scalar, pA[1] + vectAB[1] * scalar)


def find_closest(my_list, point):
    """Find the closest point of the boundaries of a polygon represented by my_list to the point passed as second parameter"""
    first = my_list[0]
    second = my_list[len(my_list) - 1]
    minimum = [find_projection(first, second, point)]
    minimum.append(distance_tuple(point, minimum[0]))
    for i in range(len(my_list) - 1):
        first = my_list[i]
        second = my_list[i + 1]
        proj = find_projection(first, second, point)
        dist = distance_tuple(point, proj)
        if dist < minimum[1]:
            minimum = [proj, dist]
    # TODO : Take into account the fact that the cone is cut
    return S.Point(minimum[0][0], minimum[0][1])


def in_half_plane(origin, orthogonal, point):
    if (point.x - origin.x) * orthogonal.x + (point.y - origin.y) * orthogonal.y >= 0.000001:
        return True
    return False
   
    
def intersection_line_line(origin1, ortho, point1, point2):
    """This function makes an intersection between two lines with the following representations:
    line1 : origin1 + ortho (vector that is normal to the line)
    line2 : two points
    """
    vect1 = S.Point(point1.x - point2.x, point1.y - point2.y)
    if vect1.x * ortho.x + vect1.y * ortho.y:
        return []
    origin2 = S.Point(origin1.x + ortho.y, origin1.y - ortho.x)
    px = (origin1.x * origin2.y - origin1.y * origin2.x) * (point1.x - point2.x) - (point1.x * point2.y - point1.y * point2.x) * (origin1.x - origin2.x)
    px /= (origin1.x - origin2.x) * (point1.y - point2.y) - (origin1.y - origin2.y) * (point1.x - point2.x)
    py = (origin1.y * origin2.x - origin1.x * origin2.y) * (point1.y - point2.y) - (point1.y * point2.x - point1.x * point2.y) * (origin1.y - origin2.y)
    py /= (origin1.y - origin2.y) * (point1.x - point2.x) - (origin1.x - origin2.x) * (point1.y - point2.y)
    return [S.Point(px, py)]
    

def half_plane(origin, orthogonal, vmax):
    """Create the intersection of the half plane starting at point facing the direction given by orthogonal with the square  of 'radius' vmax"""
    end_points = [S.Point(-vmax, -vmax), S.Point(vmax, -vmax), S.Point(vmax, vmax), S.Point(-vmax, vmax)]  # Boundaries of the square
    points = []
    for p in end_points:
        if in_half_plane(origin, orthogonal, p):
            points.append(p)
    for i in range(4):
        for p in intersection_line_line(origin, orthogonal, end_points[i], end_points[(i + 1) % 4]):
            points.append(p)
    points.sort(key=lambda x: argument(x))
    return S.Polygon(points)
