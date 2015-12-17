import sympy


# You shall not pass!!!!
    
    def is_disable_node(self, node):
        for exclusion in self.mine_field:
            if exclusion.encloses_point(Point(node.x, node.y)):
                node.disable = True
                return 0
    
    def is_disable_edge(self, edge, radius):
        
