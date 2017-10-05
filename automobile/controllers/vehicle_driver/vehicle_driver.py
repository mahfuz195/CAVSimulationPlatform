"""vehicle_driver controller."""

import math
import os
import sys

try:
    libraryPath = os.environ.get("WEBOTS_HOME") + "/projects/automobile/libraries/python"
    libraryPath.replace('/', os.sep)
    sys.path.append(libraryPath)
    from automobile import Driver
except ImportError:
    sys.stderr.write("Warning: 'automobile' module not found.\n")
    sys.exit(0)

driver = Driver()
driver.setSteeringAngle(0.2)
driver.setCruisingSpeed(20)

while driver.step() != -1:
    angle = 0.3 * math.cos(driver.getTime())
    driver.setSteeringAngle(angle)
