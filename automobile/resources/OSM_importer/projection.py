"""This module contains the Projection class."""

import math
import sys

try:
    import pyproj
except:
    sys.exit("Error: pyproj python module not installed. You can install it using pip: 'pip install pyproj'")


class Projection(object):
    """Class defining the projection used."""

    projection = None
    projectionString = ""

    @staticmethod
    def getProjection():
        """Return the projection used."""
        if Projection.projection is None:
            sys.stderr.write("Warning: Projection.getProjection() called before Projection.initProjection()\n")
        return Projection.projection

    @staticmethod
    def getProjectionString():
        """Return the projection used as a string."""
        if Projection.projection is None:
            sys.stderr.write("Warning: Projection.getProjection() called before Projection.initProjection()\n")
        return Projection.projectionString

    @staticmethod
    def project(long, lat):
        """Return a projected coordinate."""
        if Projection.projection is None:
            sys.stderr.write("Warning: Projection.project() called before Projection.initProjection()\n")
        return Projection.projection(long, lat)

    @staticmethod
    def initProjection(long0, lat0, projection):
        """Initialize the projection."""
        if projection == "":
            # WARNING: this default UTM projection should match the one of Webots GPS model
            utm_zone = 1 + math.floor((float(long0) + 180) / 6)
            hemisphere = 'south' if lat0 < 0 else 'north'
            Projection.projectionString = "+proj=utm +%s +zone=%d +lon_0=%f +lat_0=%f +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs" % (hemisphere, utm_zone, long0, lat0)
        else:
            Projection.projectionString = projection
        Projection.projection = pyproj.Proj(Projection.projectionString)
