import shapely.geometry as S


class PathEnvironnement:
    """The class independant from Blender describing the environment in which the crowd moves"""
    def __init__(self, ground, mine_field):
        self.ground = ground
        self.mine_field = mine_field  # mine_field is a set of forbidden surfaces

    def intersection_not_empty(obj1, obj2):
        """Returns true if the intersection of the objects is empty, false otherwise"""
        intersection = obj1.intersection(obj2)
        if intersection.is_empty:
            return False
        else:
            return True

    def intersect_mine_field(self, point1, point2, t):
        """Returns true if the line from point1 to point2 of thickness t intersect the mine_field"""
        line = S.LineString(point1, point2)
        line = line.buffer(t)
        return intersection_not_empty(line, self.mine_field)

    def is_disable_node(self, node):
        for exclusion in self.mine_field:
            if exclusion.encloses_point(Point(node.x, node.y)):
                node.disable = True
                return 0
