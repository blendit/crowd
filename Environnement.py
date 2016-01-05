import shapely


class PathEnvironnement:
    """The class independant from Blender describing the environment in which the crowd moves"""
    def __init__(self, ground, mine_field):
        self.ground = ground
        self.mine_field = mine_field # mine_field is a set of forbidden surfaces




# You shall not pass!!!!
    
    def is_disable_node(self, node):
        for exclusion in self.mine_field:
            if exclusion.encloses_point(Point(node.x, node.y)):
                node.disable = True
                return 0
    
    def is_disable_edge(self, edge, radius):
        
