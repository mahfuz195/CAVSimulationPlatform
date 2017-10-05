"""Contains the Tree class."""

from webots_object import WebotsObject
from road import Road

import math
import random


class Tree(WebotsObject):
    """Tree class representing an isolated tree."""

    list = []
    needleLeavesTypes = ["spruce", "white pine"]
    boardLeavesTypes = ["birch tree", "cherry tree", "crab apple tree", "hackberry tree", "hazel tree", "oak tree"]

    def __init__(self):
        """Export all the trees from the trees list."""
        self.tags = ""
        self.coord = None
        self.height = None
        self.radius = None
        self.leafType = None

    @classmethod
    def export(cls, file):
        """Export all the trees from the trees list."""
        for tree in Tree.list[:]:

            if WebotsObject.removalRadius > 0.0:
                # Check that the tree is inside the scope of a road,
                # otherwise, remove it from the tree list.
                if not Road.are_coords_close_to_some_road_waypoint([[tree.coord.x, tree.coord.z]], areOSMReferences=False):
                    Tree.list.remove(tree)
                    continue

            file.write("SimpleTree {\n")
            if tree.leafType == "needleleaved":
                file.write(' type "%s"\n' % random.choice(Tree.needleLeavesTypes))
            elif tree.leafType == "boardleaved":
                file.write(' type "%s"\n' % random.choice(Tree.boardLeavesTypes))
            else:
                file.write("  type \"random\"\n")
            file.write("  rotation 0 1 0 %.3f\n" % (random.random() * 2 * math.pi))
            file.write("  translation %.2f %.2f %.2f\n" % (tree.coord.x, tree.coord.y, tree.coord.z))
            file.write("  enableBoundingObject FALSE\n")
            if tree.height is not None:
                file.write("  height %.3f\n" % (tree.height))
            if tree.radius is not None:
                file.write("  radius %.3f\n" % (tree.radius))
            elif tree.height is not None:
                file.write("  radius %.3f\n" % (tree.height / 2.0))
            file.write("}\n")
