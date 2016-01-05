import shapely


class PathEnvironnement:
    """The class independant from Blender describing the environment in which the crowd moves"""
    def __init__(self, ground, mine_field):
        self.ground = ground
        self.mine_field = mine_field # mine_field is a set of forbidden surfaces




# You shall not pass!!!!
    
    def is_disable_node(self, node):
    
    def is_disable_edge(self, edge):
