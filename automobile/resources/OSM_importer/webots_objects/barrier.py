"""Contains the Barrier class."""

from webots_object import WebotsObject
from road import Road
from settings import Settings
from osm_objects import OSMCoord
from utils.misc_utils import extract_float_from_string, length2D


class Barrier(WebotsObject):
    """Barrier class representing a barrier segment."""

    list = []

    def __init__(self):
        """Initialize the barrier."""
        self.OSMID = 0
        self.type = ""
        self.ref = 0
        self.height = 1.5
        self.width = 0.2

    def length(self):
        """Return the length of a barrier."""
        length = 0
        for index in range(len(self.ref)):
            if index > 0:
                x = OSMCoord.coordDictionnary[self.ref[index]].x - OSMCoord.coordDictionnary[self.ref[index - 1]].x
                z = OSMCoord.coordDictionnary[self.ref[index]].z - OSMCoord.coordDictionnary[self.ref[index - 1]].z
                length = length + length2D(x, z)
        return length

    @staticmethod
    def add_to_list(osmid, tags, ref):
        """Add a new barrier to the list of barriers."""
        if 'barrier' in tags:
            settingsSection = Settings.get_section('barrier', tags['barrier'])
            if settingsSection is None:
                return
            if Settings.has_option(settingsSection, 'ignore') and Settings.get(settingsSection, 'ignore') == 'TRUE':
                return
            barrier = Barrier()
            barrier.OSMID = osmid
            barrier.type = tags['barrier']
            barrier.ref = ref
            if 'height' in tags:
                barrier.height = extract_float_from_string(tags['height'])
            elif Settings.has_option(settingsSection, 'height'):
                barrier.height = Settings.getfloat(settingsSection, 'height')
            if 'width' in tags:
                barrier.width = extract_float_from_string(tags['width'])
            elif Settings.has_option(settingsSection, 'width'):
                barrier.width = Settings.getfloat(settingsSection, 'width')
            if WebotsObject.enable3D:
                barrier.ref = Barrier.add_intermediate_point_where_needed(barrier.ref)
            Barrier.list.append(barrier)

    @classmethod
    def export(cls, file):
        """Export all the barriers from the barriers list."""
        for barrier in Barrier.list[:]:
            if len(barrier.ref) < 1:
                Barrier.list.remove(barrier)
                continue

            if WebotsObject.removalRadius > 0.0:
                # Check that the barrier is inside the scope of a road,
                # otherwise, remove it from the barrier list.
                if not Road.are_coords_close_to_some_road_waypoint(barrier.ref):
                    Barrier.list.remove(barrier)
                    continue

            if barrier.type == "fence":
                file.write("Fence {\n")
                file.write("  height %.2f\n" % barrier.height)
                file.write("  path [\n")
                for ref in barrier.ref:
                    if ref in OSMCoord.coordDictionnary:
                        file.write("    %.2f %.2f %.2f,\n" % (OSMCoord.coordDictionnary[ref].x, OSMCoord.coordDictionnary[ref].y, OSMCoord.coordDictionnary[ref].z))
                    else:
                        print("Warning: node " + str(ref) + " not referenced.")
                file.write("  ]\n")
                file.write("  splineSubdivision 0\n")
                file.write("}\n")
            elif barrier.type == "wall":
                file.write("Solid {\n")
                file.write("  translation 0 %.2f 0\n" % (barrier.height / 2))
                file.write("  children [\n")
                file.write("    DEF SHAPE Shape {\n")
                file.write("      appearance Appearance {\n")
                file.write("        material Material {}\n")
                file.write("        texture ImageTexture {\n")
                file.write("          url [ \"textures/red_brick_wall.jpg\" ]\n")
                file.write("        }\n")
                file.write("        textureTransform TextureTransform {\n")
                file.write("          scale %.1f %.1f\n" % (barrier.length(), barrier.height))
                file.write("        }\n")
                file.write("      }\n")
                file.write("      geometry Extrusion {\n")
                file.write("        crossSection [\n")
                file.write("          %.2f %.2f\n" % ((barrier.width / 2), (barrier.height / 2)))
                file.write("          %.2f %.2f\n" % ((barrier.width / 2), (-barrier.height / 2)))
                file.write("          %.2f %.2f\n" % ((-barrier.width / 2), (-barrier.height / 2)))
                file.write("          %.2f %.2f\n" % ((-barrier.width / 2), (barrier.height / 2)))
                file.write("          %.2f %.2f\n" % ((barrier.width / 2), (barrier.height / 2)))
                file.write("        ]\n")
                file.write("        spine [\n")
                for ref in barrier.ref:
                    if ref in OSMCoord.coordDictionnary:
                        file.write("          %.2f %.2f %.2f,\n" % (OSMCoord.coordDictionnary[ref].x, OSMCoord.coordDictionnary[ref].y, OSMCoord.coordDictionnary[ref].z))
                    else:
                        print("Warning: node " + str(ref) + " not referenced.")
                file.write("        ]\n")
                file.write("        splineSubdivision 0\n")
                file.write("      }\n")
                file.write("    }\n")
                file.write("  ]\n")
                file.write("  boundingObject USE SHAPE\n")
                file.write("}\n")
