import numpy as np
import shapely.geometry as S
import math


def intersection_not_empty(obj1, obj2):
    """Returns true if the intersection of the objects is empty, false otherwise"""
    intersection = obj1.intersection(obj2)
    if intersection.is_empty:
        return False
    else:
        return True


# TODO : correct this for later
def find_closest_to_optimal(vopt, obj1, center, angle, vmax):
    """Find the point of the polygon obj1 (authorised speeds) at angle that is the closest to vopt"""
    xopt = vopt * math.cos(angle)
    yopt = vopt * math.sin(angle)
    p_opt = S.Point(xopt, yopt)
    if obj1.contains(p_opt):
        return p_opt
    else:
        line = S.LineString([(center.x, center.y), (vmax * math.cos(angle), vmax * math.sin(angle))])
        inter = obj1.intersection(line)
        if inter.is_empty:
            return 0  # Case where there is no solution
        x, y = inter.xy
        minimum = float("inf")
        q = S.Point(0, 0)
        for i in range(len(x)):
            p = S.Point(x[i], y[i])
            if distance(p_opt, p) < minimum:
                q = p
                minimum = distance(p_opt, p)
        if q == S.Point(0, 0):
            return 0
        else:
            return q


def dist_theta(vopt, obj1, center, angle, tau, indiv, p_goal, graph):
    """Find the energy used if the individual goes in the direction theta"""
    p_ind = find_closest_to_optimal(vopt, obj1, center, angle, indiv.vmax)
    if p_ind == 0:
        return float("inf"), S.Point(0, 0)
    vind = math.sqrt(p_ind.x * p_ind.x + p_ind.y * p_ind.y)
    dist = vind * tau
    xnew = indiv.position.x + dist * math.cos(angle)
    ynew = indiv.position.y + dist * math.sin(angle)
    L = math.sqrt((xnew - p_goal.x) * (xnew - p_goal.x) + (ynew - p_goal.y) * (ynew - p_goal.y))  # Result of A*
    # L = graph.find_graph_distance(p_ind, p_goal)
    # FIXME : This minimization function causes problems since it does not take into account the fact that we cannot go strait forward.
    energy = tau * (indiv.es + indiv.ew * vind * vind) + 2 * L * math.sqrt(indiv.es * indiv.ew)
    return energy, p_ind


def best_angle(vopt, obj1, center, tau, dtheta, indiv, goal, graph):
    """Find the best angle and the speed vector corresponding"""
    act_ang = 0.
    min_energy, v = dist_theta(vopt, obj1, center, act_ang, tau, indiv, goal, graph)
    while (act_ang < 2 * math.pi):
        act_ang += dtheta
        energy, v_poss = dist_theta(vopt, obj1, center, act_ang, tau, indiv, goal, graph)
        if energy < min_energy:
            min_energy = energy
            v = v_poss
    return v


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
    d = (point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2
    d = math.sqrt(d)
    return d


def distance_tuple(point1, point2):
    """Euclidian Distance between two points"""
    d = (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2
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
        # print("Truncated cone :\n\t center ", center, "\n\t radius =", radius)
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

    def in_cone(self, point):
        point1 = self.limit_points[0]
        point2 = self.limit_points[1]
        angle_ref = angle(point1, point2)
        if angle_ref > math.pi:
            point1, point2 = point2, point1
        angle_ref = angle(point1, point2)
        angle1 = angle(point1, point)
        if angle1 > angle_ref:
            return False
        # The point is in the cone but might not be in the truncated cone
        line1 = S.LineString([(point.x, point.y), (0, 0)])
        if intersection_not_empty(line1, self.arc):
            return True
        return False

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


def in_half_plane(origin, orthogonal, point):
    if (point.x - origin.x) * orthogonal.x + (point.y - origin.y) * orthogonal.y >= -0.000001:
        return True
    return False


def intersection_line_line(origin1, ortho, point1, point2, vmax):
    """This function makes an intersection between two lines with the following representations:
    line1 : origin1 + ortho (vector that is normal to the line)
    line2 : two points
    Return the list of intersection points (empty or of cardinal 1)
    """
    # print(origin1, ortho, point1, point2)
    # Direction vector of the second line
    vect1 = S.Point(point1.x - point2.x, point1.y - point2.y)
    # Test if the lines are colinear or not
    # print(vect1.x * ortho.x + vect1.y * ortho.y)
    if abs(vect1.x * ortho.x + vect1.y * ortho.y) < 0.000001:
        return []
    # Find a second point on the first line
    origin2 = S.Point(origin1.x + ortho.y, origin1.y - ortho.x)
    # print(origin2)
    # Compute the intersection with an ugly forumla
    px = (origin1.x * origin2.y - origin1.y * origin2.x) * (point1.x - point2.x) - (point1.x * point2.y - point1.y * point2.x) * (origin1.x - origin2.x)
    px /= (origin1.x - origin2.x) * (point1.y - point2.y) - (origin1.y - origin2.y) * (point1.x - point2.x)
    py = (origin1.y * origin2.x - origin1.x * origin2.y) * (point1.y - point2.y) - (point1.y * point2.x - point1.x * point2.y) * (origin1.y - origin2.y)
    py /= (origin1.y - origin2.y) * (point1.x - point2.x) - (origin1.x - origin2.x) * (point1.y - point2.y)
    # Test if our intersection is within our range or not
    # print("\t", px, py)
    if abs(px) <= vmax + 0.01 and abs(py) <= vmax + 0.01:  # Needed to add an error to make sure the rest behave well
        return [S.Point(px, py)]
    else:
        return []


# TODO : Find a way to not bug if the two individual are in colision at the begining. (I.e. : if there is a bug at the begining then find a way to correct it in the end)
def half_plane(origin, orthogonal, vmax):
    """Create the intersection of the half plane starting at point facing the direction given by orthogonal with the square  of 'radius' vmax"""
    # We first verify that zero is in the half_plane
    zero = S.Point(0, 0)
    # if not in_half_plane(origin, orthogonal, zero):
    #     print("in_half_plane : Failed sanity check")
    # Boundaries of the square
    end_points = [S.Point(-vmax, -vmax), S.Point(vmax, -vmax), S.Point(vmax, vmax), S.Point(-vmax, vmax)]
    points = []
    # We add the boundaries of the square that are in the half_plane
    for p in end_points:
        if in_half_plane(origin, orthogonal, p):
            points.append(p)
    # We add the intersection points between the separation line and the sides of the square
    for i in range(4):
        # print("#intersection: ", end_points[i], end_points[(i + 1) % 4])
        for p in intersection_line_line(origin, orthogonal, end_points[i], end_points[(i + 1) % 4], vmax):
            points.append(p)
    # We order the points by there argument (0 is in the half plane by construction)
    print("\thalf_plane :\n\t\t origin = ", origin, "\n\t\t ortho = ", orthogonal, "\n\t\t vmax = ", vmax, "\n\t\t points:")
    points.sort(key=lambda x: argument(x))
    for x in points:
        print("\t\t\t", x)
    if points == []:
        return S.Point(0, 0).buffer(0.0)
    poly = S.Polygon([point_to_tuple(x) for x in points])
    print(poly)
    return S.Polygon([point_to_tuple(x) for x in points])
