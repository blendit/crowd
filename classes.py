import numpy as np
import shapely.geometry as S
import math


class Individual:
    """The class independant from Blender describing an individual"""
    def __init__(self, x, y, z, vmax, vopt, es, ew, radius):
        self.x = x
        self.y = y
        self.z = z
        self.vmax = vmax
        self.vopt = vopt
        # See the PLEdestrian paper for the meaning of this notations
        self.es = es
        self.ew = ew
        self.radius = radius
        self.trajectory = list()


class Crowd:
    """The class independant from Blender describing the crowd"""
    def __init__(self, graph):
        self.individual = set()
        self.graph = graph
