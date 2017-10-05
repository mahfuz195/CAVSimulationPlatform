"""Contains the Area class."""

from webots_object import WebotsObject
from road import Road
from settings import Settings
from osm_objects import OSMCoord

from utils.misc_utils import clean_string, protect_def_name

import os
import random


class Area(WebotsObject):
    """Area class representing for example a forest area or a water area."""

    list = []
    noForests = False

    def __init__(self):
        """Initialize the area."""
        self.OSMID = 0
        self.type = ""
        self.ref = []
        self.color = [0, 0, 0]
        self.transparency = 0
        self.texture = ""
        self.name = ""
        self.density = 0.1

    @staticmethod
    def add_to_list(osmid, type, tags, ref):
        """Add a new area to the list of areas."""
        settingsSection = Settings.get_section('area', type)
        if settingsSection is None:
            return
        area = Area()
        area.OSMID = osmid
        area.ref = ref
        area.type = type
        if 'name' in tags:
            area.name = clean_string(tags['name'])
        if Settings.has_option(settingsSection, 'texture'):
            area.texture = Settings.get(settingsSection, 'texture')
        if Settings.has_option(settingsSection, 'transparency'):
            area.transparency = Settings.getfloat(settingsSection, 'transparency')
        if Settings.has_option(settingsSection, 'redComponent'):
            area.color[0] = Settings.getfloat(settingsSection, 'redComponent')
        if Settings.has_option(settingsSection, 'greenComponent'):
            area.color[1] = Settings.getfloat(settingsSection, 'greenComponent')
        if Settings.has_option(settingsSection, 'blueComponent'):
            area.color[2] = Settings.getfloat(settingsSection, 'blueComponent')
        if Settings.has_option(settingsSection, 'density'):
            area.density = Settings.getfloat(settingsSection, 'density')
        Area.list.append(area)

    @staticmethod
    def are_references_clockwise(referenceList):
        """Check if a list of points is defined in a clockwise maner."""
        total = 0
        for i in range(0, len(referenceList)):
            total = total + (OSMCoord.coordDictionnary[referenceList[i]].x - OSMCoord.coordDictionnary[referenceList[i - 1]].x) * (OSMCoord.coordDictionnary[referenceList[i]].z + OSMCoord.coordDictionnary[referenceList[i - 1]].z)
        if total >= 0:
            return True
        else:
            return False

    @staticmethod
    def is_point_in_polygon(x, z, polygon):
        """Determine if a point is inside a given polygon or not."""
        """Polygon is a list of (x,z) pairs."""
        n = len(polygon)
        inside = False
        p1x, p1z = polygon[0]
        for i in range(n + 1):
            p2x, p2z = polygon[i % n]
            if z > min(p1z, p2z):
                if z <= max(p1z, p2z):
                    if x <= max(p1x, p2x):
                        if p1z != p2z:
                            xinters = (z - p1z) * (p2x - p1x) / (p2z - p1z) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1z = p2x, p2z
        return inside

    @staticmethod
    def draw_area(file, refs, red=1, green=0, blue=0, defName="", transparency=0.0, texture="", drawFlat=False, verticalOffset=0.0):
        """Draw an area."""
        if len(refs) < 3:
            return
        if not defName == "":
            file.write("DEF " + defName + " " + "Transform {\n")
        else:
            file.write("Transform {\n")
        file.write("  translation %f 0 %f\n" % (OSMCoord.coordDictionnary[refs[0]].x, OSMCoord.coordDictionnary[refs[0]].z))
        file.write("  children [\n")
        file.write("    Shape {\n")
        file.write("      appearance Appearance {\n")
        file.write("        material Material {\n")
        file.write("          diffuseColor " + str(red) + " " + str(green) + " " + str(blue) + "\n")
        if transparency > 0:
            file.write("          transparency " + str(transparency) + "\n")
        file.write("        }\n")
        if not texture == "":
            file.write("        texture ImageTexture {\n")
            file.write("          url [\n")
            file.write("            \"" + texture + "\"\n")
            file.write("          ]\n")
            file.write("        }\n")
            xMin, xMax, zMin, zMax = OSMCoord.get_min_and_max_coord(refs)
            scale = max(abs(round(xMax - xMin)), abs(round(zMax - zMin)))
            file.write("        textureTransform TextureTransform {\n")
            file.write("          scale %.2f %.2f\n" % (scale, scale))
            file.write("        }\n")
        file.write("      }\n")
        file.write("      geometry IndexedFaceSet {\n")
        file.write("        coord Coordinate {\n")
        file.write("          point [\n")
        if drawFlat:
            height = 0
            for ref in refs:
                if ref in OSMCoord.coordDictionnary:
                    height = height + OSMCoord.coordDictionnary[ref].y
            height = height / len(refs)
        for ref in refs:
            if ref in OSMCoord.coordDictionnary:
                if drawFlat:
                    file.write("            %.2f %.2f %.2f,\n" % (OSMCoord.coordDictionnary[ref].x - OSMCoord.coordDictionnary[refs[0]].x, height + verticalOffset, OSMCoord.coordDictionnary[ref].z - OSMCoord.coordDictionnary[refs[0]].z))
                else:
                    file.write("            %.2f %.2f %.2f,\n" % (OSMCoord.coordDictionnary[ref].x - OSMCoord.coordDictionnary[refs[0]].x, OSMCoord.coordDictionnary[ref].y + verticalOffset, OSMCoord.coordDictionnary[ref].z - OSMCoord.coordDictionnary[refs[0]].z))
            else:
                print("Warning: node " + str(ref) + " not referenced.")
        file.write("          ]\n")
        file.write("        }\n")
        if Area.are_references_clockwise(refs) is False:
            file.write("        ccw FALSE\n")
        file.write("        coordIndex [\n")
        for i in range(0, len(refs)):
            file.write("          " + str(i) + "\n")
        file.write("          -1\n")
        file.write("        ]\n")
        file.write("      }\n")
        file.write("      castShadows FALSE\n")
        file.write("    }\n")
        file.write("  ]\n")
        file.write("}\n")

    @classmethod
    def export(cls, file, noParkings):
        """Export all the areas from the areas list."""
        for area in Area.list[:]:
            if noParkings and area.type == 'parking':
                Area.list.remove(area)
                continue

            if WebotsObject.removalRadius > 0.0:
                # Check that the area is inside the scope of a road,
                # otherwise, remove it from the area list.
                if not Road.are_coords_close_to_some_road_waypoint(area.ref):
                    Area.list.remove(area)
                    continue

            defName = ""
            if not area.name == "":
                defName = area.name
            else:
                defName = area.type
            defName = protect_def_name(defName)
            if area.type == 'forest' and not Area.noForests:
                treesFile = area.generate_tree_file(os.path.dirname(os.path.abspath(file.name)))
                if file is not None:
                    file.write("Forest {\n")
                    file.write("  treesFiles [\n")
                    file.write("    " + "\"" + treesFile + "\"" + "\n")
                    file.write("  ]\n")
                    file.write("}\n")
            else:
                verticalOffset = -0.01 if area.type == 'parking' else 0.0
                drawFlat = True if area.type == 'water' else False
                Area.draw_area(file, area.ref, area.color[0], area.color[1], area.color[2], defName, area.transparency, area.texture, verticalOffset=verticalOffset, drawFlat=drawFlat)

    def generate_tree_file(self, folder):
        """Generate the 'forest' file which contains the tree positions and is used by the 'Forest' PROTO."""
        treeNumber = 0
        polygon = []
        xMin, xMax, zMin, zMax = OSMCoord.get_min_and_max_coord(self.ref)
        for ref in self.ref:
            polygon.append([OSMCoord.coordDictionnary[ref].x, OSMCoord.coordDictionnary[ref].z])

        numberOfTree = int(round((xMax - xMin) * (zMax - zMin)) * self.density)
        if not os.path.exists(folder + '/forest'):
            os.makedirs(folder + '/forest')
        file = open(folder + '/forest/' + str(self.OSMID) + '.forest', 'w')
        for index in range(0, numberOfTree):
            x = random.uniform(xMin, xMax)
            z = random.uniform(zMin, zMax)
            y = 0
            if WebotsObject.elevation is not None:
                y = WebotsObject.elevation.interpolate_height(-x + WebotsObject.xOffset, z + WebotsObject.zOffset)
            if Area.is_point_in_polygon(x, z, polygon) is True:
                treeNumber = treeNumber + 1
                file.write("%.2f,%.2f,%.2f\n" % (x, y, z))
        file.close()
        if treeNumber > 0:
            return 'forest/' + str(self.OSMID) + '.forest'
        else:
            os.remove('forest/' + str(self.OSMID) + '.forest')
            return None
