"""Contains the Building class."""

from webots_object import WebotsObject
from road import Road
from utils.misc_utils import extract_float_from_string
from settings import Settings
from osm_objects import OSMCoord


class Building(WebotsObject):
    """Building class representing one building."""

    list = []

    def __init__(self):
        """Initialize the building."""
        self.OSMID = 0
        self.type = ""
        self.ref = []
        self.name = ""
        self.number = ""
        self.layer = 0.0
        self.levels = -1
        self.height = -1
        self.roofHeight = -1
        self.roofShape = ""

    @staticmethod
    def add_to_list(osmid, tags, ref):
        """Add a new building to the list of buildings."""
        if 'building' in tags:
            building = Building()
            building.OSMID = osmid
            building.type = tags['building']
            if 'name' in tags:
                building.name = tags['name']
            elif 'ref' in tags:
                building.name = tags['ref']
            if 'roof:height' in tags:
                building.roofHeight = extract_float_from_string(tags['roof:height'])
            if 'height' in tags:
                if building.roofHeight > 0:
                    building.height = extract_float_from_string(tags['height']) - building.roofHeight
                else:
                    building.height = extract_float_from_string(tags['height'])
            if 'roof:shape' in tags:
                building.roofShape = tags['roof:shape']
            if 'layer' in tags:
                building.layer = extract_float_from_string(tags['layer'])
            if 'building:levels' in tags:
                building.levels = int(extract_float_from_string(tags['building:levels']))
            building.ref = ref
            if len(building.ref) > 0 and building.ref[0] == building.ref[-1]:  # often last and first reference are the same => this is useless for us
                del building.ref[-1]
            Building.list.append(building)

    @classmethod
    def export(cls, file):
        """Export all the buildings from the buildings list."""
        for building in Building.list[:]:
            settingsSection = Settings.get_section('building', building.type)
            if settingsSection is None or len(building.ref) < 1:
                Building.list.remove(building)
                continue

            if WebotsObject.removalRadius > 0.0:
                # Check that the building is inside the scope of a road,
                # otherwise, remove it from the building list.
                if not Road.are_coords_close_to_some_road_waypoint(building.ref):
                    Building.list.remove(building)
                    continue

            file.write("SimpleBuilding {\n")
            # set the height of the building to be the height of the minimum corner
            if WebotsObject.enable3D:
                height = float('inf')
                for ref in building.ref:
                    if ref in OSMCoord.coordDictionnary and OSMCoord.coordDictionnary[ref].y < height:
                        height = OSMCoord.coordDictionnary[ref].y
                if height == float('inf'):
                    height = 0
                height = height + building.layer * WebotsObject.layerHeight
                file.write("  translation %.2lf %.2lf %.2lf\n" % (OSMCoord.coordDictionnary[building.ref[0]].x, height, OSMCoord.coordDictionnary[building.ref[0]].z))
            else:
                file.write("  translation %.2lf %.2lf %.2lf\n" % (OSMCoord.coordDictionnary[building.ref[0]].x, building.layer * WebotsObject.layerHeight, OSMCoord.coordDictionnary[building.ref[0]].z))

            name = building.name
            if name != '' and building.number != '':
                name += ' ' + building.number
            name = name.replace('"', '')
            if name != '':
                file.write('  name "%s"\n' % name)

            file.write("  corners [\n")
            for ref in building.ref:
                if ref in OSMCoord.coordDictionnary:
                    file.write("    %.2f %.2f,\n" % (OSMCoord.coordDictionnary[ref].x - OSMCoord.coordDictionnary[building.ref[0]].x, OSMCoord.coordDictionnary[ref].z - OSMCoord.coordDictionnary[building.ref[0]].z))
                else:
                    print("Warning: node " + str(ref) + " not referenced.")
            file.write("  ]\n")
            if building.roofShape == 'pyramidal':
                file.write("  roofShape \"pyramidal roof\"\n")
            elif building.roofShape == 'flat':
                file.write("  roofShape \"flat roof\"\n")
            else:
                if len(building.ref) <= 4:
                    file.write("  roofShape \"pyramidal roof\"\n")
                else:
                    file.write("  roofShape \"flat roof\"\n")
            if building.roofHeight > 0:
                file.write("  roofHeight %.2f\n" % building.roofHeight)
            if building.levels > 0:
                file.write("  floorNumber " + str(building.levels) + "\n")
            elif Settings.has_option(settingsSection, 'floorNumber'):
                building.levels = Settings.getfloat(settingsSection, 'floorNumber')
                file.write("  floorNumber " + Settings.get(settingsSection, 'floorNumber') + "\n")
            if building.height > 0:
                if building.levels > 0:
                    file.write("  floorHeight %.2f\n" % (building.height / building.levels))
                else:
                    file.write("  floorHeight %.2f\n" % (building.height / 3))
            elif Settings.has_option(settingsSection, 'floorHeight'):
                file.write("  floorHeight " + Settings.get(settingsSection, 'floorHeight') + "\n")
            if Settings.has_option(settingsSection, 'wallType'):
                file.write("  wallType " + Settings.get(settingsSection, 'wallType') + "\n")
            else:
                file.write("  wallType \"random\"\n")
            if Settings.has_option(settingsSection, 'roofType'):
                file.write("  roofType " + Settings.get(settingsSection, 'roofType') + "\n")
            if Settings.has_option(settingsSection, 'roofShape'):
                file.write("  roofShape " + Settings.get(settingsSection, 'roofShape') + "\n")
            if Settings.has_option(settingsSection, 'roofHeight'):
                file.write("  roofHeight " + Settings.getfloat(settingsSection, 'roofHeight') + "\n")
            if building.layer > 0:
                file.write("  bottom TRUE\n")
            file.write("}\n")
