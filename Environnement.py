import shapely.geometry as S


class PathEnvironnement:
    """The class independant from Blender describing the environment in which the crowd moves"""
    def __init__(self, ground, mine_field):
        self.ground = ground
        self.mine_field = mine_field  # mine_field is a set of forbidden surfaces

    def intersection_not_empty(obj1, obj2):
        """This function return true if the intersection of the objects is empty, false otherwise"""
        intersection = obj1.intersection(obj2)
        if intersection.is_empty:
            return 0
        else:
            return 1
    
    def is_disable_node(self, node):
        for exclusion in self.mine_field:
            if exclusion.encloses_point(Point(node.x, node.y)):
                node.disable = True
                return 0
