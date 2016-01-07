import shapely.geometry as S
import math


def argument(point):
    """Gives the complex argument of a point in the plane"""
    return math.atan2(point.y, point.x)
   
 
def angle(p1, p2):
    """Gives the value of the angle represented by the two points"""
    theta1 = argument(p1)
    theta2 = argument(p2)
    theta = theta2 - theta1
    if theta < - 2 * math.pi:
        theta = theta + 2 * math.pi
    return theta

 
def create_cone(point1, point2, dmax):
    """Create a polygon representing a cone. It starts at 0 and the 2 limits of the cone are given by the two points, the angle is also smaller than Pi. Moreover this cone is intersected with a square given by dmax"""
    theta1 = argument(point1)
    theta2 = argument(point2)
    vertices = [S.Point(0, 0)]  # Our cone
    z = max(point1.x, point1.y)
    verticies.append(S.Point(point1.x / z * dmax, point1.y / z * dmax))
    end_points = [S.Point(-dmax, -dmax), S.Point(dmax, -dmax), S.Point(dmax, dmax), S.Point(-dmax, dmax)]  # Boundaries of the square
    # We start looking for the corners of the square that are in the cone
    if theta1 < theta2:  # Normal case (i.e. no trigonometric problems)
        for i in range(1, 4):
            if argument(end_points[i]) > theta1 and argument(end_points[i]) < theta2:
                verticies.append(end_points[i])
    else:  # theta2 <= theta1 (trigonomtric problem: we pass from Pi to -Pi "continuously")
        adding = False
        for i in range(1, 4):
            if angle(point1, end_points[i]) > 0 and angle(point1, end_points[i]) < angle(point1, point2) and adding:
                verticies.append(end_points[i])
            else:
                adding = True
        adding = True
        for i in range(1, 4):
            if angle(point1, end_points[i]) > 0 and angle(point1, end_points[i]) < angle(point1, point2) and adding:
                verticies.append(end_points[i])
            else:
                adding = False
    # We finshed adding the corners in the right order. Only left is the last point.
    z = max(point2.x, point2.y)
    verticies.append(S.Point(point2.x / z * dmax, point2.y / z * dmax))
